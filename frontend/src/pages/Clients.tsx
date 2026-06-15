import { useEffect, useState, type FormEvent } from "react";
import { Plus, Search } from "lucide-react";
import { Header } from "../components/Header";
import { Modal } from "../components/Modal";
import { LoadingSpinner, EmptyState } from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { api, ApiError } from "../api/client";
import type { Client } from "../types";

export function ClientsPage() {
  const { isStaff } = useAuth();
  const { toast } = useToast();
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ nome_completo: "", email: "", telefone: "", cpf: "", endereco: "" });

  const load = () => {
    setLoading(true);
    api.getClients()
      .then(setClients)
      .catch(() => toast("Erro ao carregar tutores", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = clients.filter(
    (c) =>
      c.nome_completo.toLowerCase().includes(search.toLowerCase()) ||
      c.email.toLowerCase().includes(search.toLowerCase()),
  );

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.createClient(form);
      toast("Tutor cadastrado com sucesso!");
      setModalOpen(false);
      setForm({ nome_completo: "", email: "", telefone: "", cpf: "", endereco: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao cadastrar", "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header title="Tutores" subtitle="Cadastro de clientes e responsáveis pelos animais" />

      <div className="mb-6 flex flex-wrap items-center gap-4">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por nome ou e-mail..."
            className="input-field pl-10"
          />
        </div>
        {isStaff && (
          <button onClick={() => setModalOpen(true)} className="btn-primary">
            <Plus size={18} /> Novo tutor
          </button>
        )}
      </div>

      <div className="card overflow-hidden !p-0">
        {loading ? (
          <LoadingSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState message="Nenhum tutor encontrado" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/80 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <th className="px-6 py-3">Nome</th>
                  <th className="px-6 py-3">E-mail</th>
                  <th className="px-6 py-3">Telefone</th>
                  <th className="px-6 py-3">CPF</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {filtered.map((c) => (
                  <tr key={c.id} className="transition hover:bg-warm-200/80">
                    <td className="px-6 py-4 font-medium text-slate-800">{c.nome_completo}</td>
                    <td className="px-6 py-4 text-slate-600">{c.email}</td>
                    <td className="px-6 py-4 text-slate-600">{c.telefone}</td>
                    <td className="px-6 py-4 text-slate-600">{c.cpf}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Cadastrar tutor">
        <form onSubmit={handleSubmit} className="space-y-4">
          {(["nome_completo", "email", "telefone", "cpf"] as const).map((field) => (
            <div key={field}>
              <label className="mb-1 block text-sm font-medium capitalize text-slate-700">
                {field === "nome_completo" ? "Nome completo" : field}
              </label>
              <input
                type={field === "email" ? "email" : "text"}
                value={form[field]}
                onChange={(e) => setForm({ ...form, [field]: e.target.value })}
                className="input-field"
                required
              />
            </div>
          ))}
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Endereço</label>
            <textarea
              value={form.endereco}
              onChange={(e) => setForm({ ...form, endereco: e.target.value })}
              className="input-field"
              rows={2}
              required
            />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={() => setModalOpen(false)} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-primary">{saving ? "Salvando..." : "Cadastrar"}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
