import { useEffect, useState, type FormEvent } from "react";
import { Plus, Search } from "lucide-react";
import { Header } from "../components/Header";
import { Modal } from "../components/Modal";
import { LoadingSpinner, EmptyState } from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { api, ApiError } from "../api/client";
import type { Veterinarian } from "../types";

export function VeterinariansPage() {
  const { isStaff } = useAuth();
  const { toast } = useToast();
  const [vets, setVets] = useState<Veterinarian[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    crmv: "",
    specialty: "",
  });

  const load = () => {
    setLoading(true);
    api
      .getVeterinarians()
      .then(setVets)
      .catch((err) => toast(err instanceof ApiError ? err.message : "Erro ao carregar veterinários", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = vets.filter(
    (v) =>
      v.full_name.toLowerCase().includes(search.toLowerCase()) ||
      v.crmv.toLowerCase().includes(search.toLowerCase()) ||
      v.specialty.toLowerCase().includes(search.toLowerCase()),
  );

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const auth = await api.register({
        email: form.email,
        password: form.password,
        full_name: form.full_name,
        role: "veterinarian",
      });
      await api.createVeterinarian({
        user_id: auth.user_id,
        full_name: form.full_name,
        crmv: form.crmv,
        specialty: form.specialty,
      });
      toast("Veterinário cadastrado com sucesso!");
      setModalOpen(false);
      setForm({ full_name: "", email: "", password: "", crmv: "", specialty: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao cadastrar veterinário", "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header
        title="Veterinários"
        subtitle="Equipe clínica — necessário para agendar consultas e vacinas"
      />

      <div className="mb-6 flex flex-wrap items-center gap-4">
        <div className="relative min-w-[200px] flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por nome, CRMV ou especialidade..."
            className="input-field pl-10"
          />
        </div>
        {isStaff && (
          <button onClick={() => setModalOpen(true)} className="btn-primary">
            <Plus size={18} /> Novo veterinário
          </button>
        )}
      </div>

      <div className="card overflow-hidden !p-0">
        {loading ? (
          <LoadingSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState message="Nenhum veterinário cadastrado. Cadastre um para agendar consultas." />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/80 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <th className="px-6 py-3">Nome</th>
                  <th className="px-6 py-3">CRMV</th>
                  <th className="px-6 py-3">Especialidade</th>
                  <th className="px-6 py-3">Cadastro</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {filtered.map((v) => (
                  <tr key={v.id} className="transition hover:bg-warm-200/80">
                    <td className="px-6 py-4 font-medium text-slate-800">{v.full_name}</td>
                    <td className="px-6 py-4 text-slate-600">{v.crmv}</td>
                    <td className="px-6 py-4 text-slate-600">{v.specialty}</td>
                    <td className="px-6 py-4 text-slate-600">
                      {new Date(v.created_at).toLocaleDateString("pt-BR")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Cadastrar veterinário">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Nome completo</label>
            <input
              type="text"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              className="input-field"
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">E-mail (acesso ao sistema)</label>
            <input
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="input-field"
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Senha inicial</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="input-field"
              minLength={8}
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">CRMV</label>
            <input
              type="text"
              value={form.crmv}
              onChange={(e) => setForm({ ...form, crmv: e.target.value })}
              className="input-field"
              placeholder="SP-12345"
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Especialidade</label>
            <input
              type="text"
              value={form.specialty}
              onChange={(e) => setForm({ ...form, specialty: e.target.value })}
              className="input-field"
              placeholder="Clínica Geral"
              required
            />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={() => setModalOpen(false)} className="btn-secondary">
              Cancelar
            </button>
            <button type="submit" disabled={saving} className="btn-primary">
              {saving ? "Salvando..." : "Cadastrar"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
