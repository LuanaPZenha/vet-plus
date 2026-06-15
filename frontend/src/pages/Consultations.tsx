import { useEffect, useState, type FormEvent } from "react";
import { Plus, CheckCircle } from "lucide-react";
import { Header } from "../components/Header";
import { Modal } from "../components/Modal";
import { LoadingSpinner, EmptyState } from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { api, ApiError } from "../api/client";
import type { Consultation, Animal, Veterinarian } from "../types";

const statusLabels: Record<string, { label: string; class: string }> = {
  scheduled: { label: "Agendada", class: "bg-blue-100 text-blue-700" },
  in_progress: { label: "Em andamento", class: "bg-amber-100 text-amber-700" },
  completed: { label: "Concluída", class: "bg-accent-500/15 text-accent-600" },
  cancelled: { label: "Cancelada", class: "bg-slate-100 text-slate-600" },
};

const typeLabels: Record<string, string> = {
  regular: "Consulta regular",
  emergency: "Emergência",
  surgery: "Cirurgia",
};

export function ConsultationsPage() {
  const { isStaff } = useAuth();
  const { toast } = useToast();
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [vets, setVets] = useState<Veterinarian[]>([]);
  const [loading, setLoading] = useState(true);
  const [scheduleModal, setScheduleModal] = useState(false);
  const [completeModal, setCompleteModal] = useState<Consultation | null>(null);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    animal_id: "", veterinarian_id: "", scheduled_at: "", type: "regular", notes: "",
  });
  const [completeForm, setCompleteForm] = useState({ diagnosis: "", prescription_notes: "" });

  const load = () => {
    setLoading(true);
    Promise.all([api.getConsultations(), api.getAnimals(), api.getVeterinarians()])
      .then(([c, a, v]) => { setConsultations(c); setAnimals(a); setVets(v); })
      .catch(() => toast("Erro ao carregar consultas", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleSchedule = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.createConsultation({
        animal_id: Number(form.animal_id),
        veterinarian_id: Number(form.veterinarian_id),
        scheduled_at: new Date(form.scheduled_at).toISOString(),
        type: form.type,
        notes: form.notes,
      });
      toast("Consulta agendada com sucesso!");
      setScheduleModal(false);
      setForm({ animal_id: "", veterinarian_id: "", scheduled_at: "", type: "regular", notes: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao agendar", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleComplete = async (e: FormEvent) => {
    e.preventDefault();
    if (!completeModal) return;
    setSaving(true);
    try {
      await api.completeConsultation(completeModal.id, completeForm);
      toast("Consulta concluída com sucesso!");
      setCompleteModal(null);
      setCompleteForm({ diagnosis: "", prescription_notes: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao concluir", "error");
    } finally {
      setSaving(false);
    }
  };

  const getAnimalName = (id: number) => animals.find((a) => a.id === id)?.name || `#${id}`;
  const getVetName = (id: number) => vets.find((v) => v.id === id)?.full_name || `#${id}`;

  return (
    <div>
      <Header title="Consultas" subtitle="Agendamento e atendimentos veterinários" />

      <div className="mb-6 flex justify-end">
        <button onClick={() => setScheduleModal(true)} className="btn-primary">
          <Plus size={18} /> Agendar consulta
        </button>
      </div>

      <div className="card overflow-hidden !p-0">
        {loading ? (
          <LoadingSpinner />
        ) : consultations.length === 0 ? (
          <EmptyState message="Nenhuma consulta registrada" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/80 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <th className="px-6 py-3">Animal</th>
                  <th className="px-6 py-3">Veterinário</th>
                  <th className="px-6 py-3">Data/Hora</th>
                  <th className="px-6 py-3">Tipo</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Preço</th>
                  {isStaff && <th className="px-6 py-3">Ações</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {consultations.map((c) => {
                  const st = statusLabels[c.status] || statusLabels.scheduled;
                  return (
                    <tr key={c.id} className="hover:bg-warm-200/80">
                      <td className="px-6 py-4 font-medium">{getAnimalName(c.animal_id)}</td>
                      <td className="px-6 py-4 text-slate-600">{getVetName(c.veterinarian_id)}</td>
                      <td className="px-6 py-4 text-slate-600">{new Date(c.scheduled_at).toLocaleString("pt-BR")}</td>
                      <td className="px-6 py-4 text-slate-600">{typeLabels[c.type] || c.type}</td>
                      <td className="px-6 py-4"><span className={`badge ${st.class}`}>{st.label}</span></td>
                      <td className="px-6 py-4 text-slate-600">{c.price ? `R$ ${c.price}` : "—"}</td>
                      {isStaff && (
                        <td className="px-6 py-4">
                          {c.status === "scheduled" && (
                            <button
                              onClick={() => setCompleteModal(c)}
                              className="flex items-center gap-1 text-xs font-medium text-accent-600 hover:text-accent-500"
                            >
                              <CheckCircle size={16} /> Concluir
                            </button>
                          )}
                        </td>
                      )}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={scheduleModal} onClose={() => setScheduleModal(false)} title="Agendar consulta">
        <form onSubmit={handleSchedule} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Animal</label>
              <select value={form.animal_id} onChange={(e) => setForm({ ...form, animal_id: e.target.value })} className="input-field" required>
                <option value="">Selecione...</option>
                {animals.map((a) => <option key={a.id} value={a.id}>{a.name}</option>)}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Veterinário</label>
              <select value={form.veterinarian_id} onChange={(e) => setForm({ ...form, veterinarian_id: e.target.value })} className="input-field" required>
                <option value="">Selecione...</option>
                {vets.map((v) => <option key={v.id} value={v.id}>{v.full_name}</option>)}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Data e hora</label>
              <input type="datetime-local" value={form.scheduled_at} onChange={(e) => setForm({ ...form, scheduled_at: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Tipo</label>
              <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })} className="input-field">
                <option value="regular">Consulta regular</option>
                <option value="emergency">Emergência</option>
                <option value="surgery">Cirurgia</option>
              </select>
            </div>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Observações</label>
            <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} className="input-field" rows={2} />
          </div>
          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => setScheduleModal(false)} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-primary">{saving ? "Agendando..." : "Agendar"}</button>
          </div>
        </form>
      </Modal>

      <Modal open={!!completeModal} onClose={() => setCompleteModal(null)} title="Concluir consulta">
        <form onSubmit={handleComplete} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Diagnóstico</label>
            <textarea value={completeForm.diagnosis} onChange={(e) => setCompleteForm({ ...completeForm, diagnosis: e.target.value })} className="input-field" rows={3} required />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Prescrição / Observações</label>
            <textarea value={completeForm.prescription_notes} onChange={(e) => setCompleteForm({ ...completeForm, prescription_notes: e.target.value })} className="input-field" rows={2} />
          </div>
          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => setCompleteModal(null)} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-primary">{saving ? "Salvando..." : "Concluir consulta"}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
