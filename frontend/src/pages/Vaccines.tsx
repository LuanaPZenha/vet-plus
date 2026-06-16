import { useEffect, useState, type FormEvent } from "react";
import { Plus, AlertTriangle } from "lucide-react";
import { Header } from "../components/Header";
import { Modal } from "../components/Modal";
import { LoadingSpinner, EmptyState } from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { api, ApiError } from "../api/client";
import type { Vaccine, Animal, Veterinarian, UpcomingVaccine } from "../types";

export function VaccinesPage() {
  const { isStaff } = useAuth();
  const { toast } = useToast();
  const [vaccines, setVaccines] = useState<Vaccine[]>([]);
  const [upcoming, setUpcoming] = useState<UpcomingVaccine[]>([]);
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [vets, setVets] = useState<Veterinarian[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    animal_id: "", vaccine_name: "", application_date: "", next_dose_date: "", veterinarian_id: "", batch_number: "",
  });

  const load = () => {
    setLoading(true);
    Promise.all([
      api.getVaccines().catch(() => [] as Vaccine[]),
      api.getUpcomingVaccines().catch(() => [] as UpcomingVaccine[]),
      api.getAnimals(),
      api.getVeterinarians().catch(() => [] as Veterinarian[]),
    ])
      .then(([v, u, a, vt]) => {
        setVaccines(v);
        setUpcoming(u);
        setAnimals(a);
        setVets(vt);
        if (a.length === 0) {
          toast("Cadastre um animal em Animais antes de registrar vacinas.", "error");
        } else if (vt.length === 0) {
          toast("Cadastre um veterinário antes de registrar vacinas.", "error");
        }
      })
      .catch(() => toast("Erro ao carregar dados. Verifique se tutores e animais estão cadastrados.", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const getAnimalName = (id: number) => animals.find((a) => a.id === id)?.name || `#${id}`;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.createVaccine({
        animal_id: Number(form.animal_id),
        vaccine_name: form.vaccine_name,
        application_date: form.application_date,
        next_dose_date: form.next_dose_date || undefined,
        veterinarian_id: Number(form.veterinarian_id),
        batch_number: form.batch_number || undefined,
      });
      toast("Vacina registrada com sucesso!");
      setModalOpen(false);
      setForm({ animal_id: "", vaccine_name: "", application_date: "", next_dose_date: "", veterinarian_id: "", batch_number: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao registrar", "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header title="Vacinas" subtitle="Controle vacinal e lembretes de doses" />

      {upcoming.length > 0 && (
        <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4">
          <div className="flex items-center gap-2 text-amber-800">
            <AlertTriangle size={20} />
            <span className="font-semibold">{upcoming.length} vacina(s) próxima(s) do vencimento</span>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            {upcoming.map((v) => (
              <span key={v.id} className="badge bg-amber-100 text-amber-800">
                {getAnimalName(v.animal_id)} — {v.vaccine_name} ({v.days_until_due}d)
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mb-6 flex justify-end">
        {isStaff && (
          <button onClick={() => setModalOpen(true)} className="btn-primary">
            <Plus size={18} /> Registrar vacina
          </button>
        )}
      </div>

      <div className="card overflow-hidden !p-0">
        {loading ? (
          <LoadingSpinner />
        ) : vaccines.length === 0 ? (
          <EmptyState message="Nenhuma vacina registrada" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/80 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <th className="px-6 py-3">Animal</th>
                  <th className="px-6 py-3">Vacina</th>
                  <th className="px-6 py-3">Aplicação</th>
                  <th className="px-6 py-3">Próxima dose</th>
                  <th className="px-6 py-3">Lote</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {vaccines.map((v) => (
                  <tr key={v.id} className="hover:bg-warm-200/80">
                    <td className="px-6 py-4 font-medium">{getAnimalName(v.animal_id)}</td>
                    <td className="px-6 py-4 text-slate-600">{v.vaccine_name}</td>
                    <td className="px-6 py-4 text-slate-600">{new Date(v.application_date).toLocaleDateString("pt-BR")}</td>
                    <td className="px-6 py-4 text-slate-600">
                      {v.next_dose_date ? new Date(v.next_dose_date).toLocaleDateString("pt-BR") : "—"}
                    </td>
                    <td className="px-6 py-4 text-slate-600">{v.batch_number || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Registrar vacina">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Animal</label>
              <select value={form.animal_id} onChange={(e) => setForm({ ...form, animal_id: e.target.value })} className="input-field" required>
                <option value="">Selecione...</option>
                {animals.map((a) => <option key={a.id} value={a.id}>{a.name}</option>)}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Vacina</label>
              <input value={form.vaccine_name} onChange={(e) => setForm({ ...form, vaccine_name: e.target.value })} className="input-field" placeholder="Ex: V10, Antirrábica" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Data aplicação</label>
              <input type="date" value={form.application_date} onChange={(e) => setForm({ ...form, application_date: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Próxima dose</label>
              <input type="date" value={form.next_dose_date} onChange={(e) => setForm({ ...form, next_dose_date: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Veterinário</label>
              <select value={form.veterinarian_id} onChange={(e) => setForm({ ...form, veterinarian_id: e.target.value })} className="input-field" required>
                <option value="">Selecione...</option>
                {vets.map((v) => <option key={v.id} value={v.id}>{v.full_name}</option>)}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Lote</label>
              <input value={form.batch_number} onChange={(e) => setForm({ ...form, batch_number: e.target.value })} className="input-field" />
            </div>
          </div>
          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => setModalOpen(false)} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-primary">{saving ? "Salvando..." : "Registrar"}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
