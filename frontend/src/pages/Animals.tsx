import { useEffect, useState, type FormEvent } from "react";
import { Plus, Search } from "lucide-react";
import { Header } from "../components/Header";
import { Modal } from "../components/Modal";
import { LoadingSpinner, EmptyState } from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { api, ApiError } from "../api/client";
import type { Animal, Client } from "../types";

const speciesEmoji: Record<string, string> = {
  cachorro: "🐕",
  gato: "🐈",
  ave: "🐦",
  coelho: "🐇",
  default: "🐾",
};

export function AnimalsPage() {
  const { isStaff } = useAuth();
  const { toast } = useToast();
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    name: "", species: "Cachorro", breed: "", birth_date: "", weight: "", client_id: "",
  });

  const load = () => {
    setLoading(true);
    Promise.all([api.getAnimals(), isStaff ? api.getClients() : Promise.resolve([])])
      .then(([a, c]) => { setAnimals(a); setClients(c); })
      .catch(() => toast("Erro ao carregar animais", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(load, [isStaff]);

  const filtered = animals.filter(
    (a) =>
      a.name.toLowerCase().includes(search.toLowerCase()) ||
      a.species.toLowerCase().includes(search.toLowerCase()),
  );

  const getEmoji = (species: string) => {
    const key = species.toLowerCase();
    return speciesEmoji[key] || speciesEmoji.default;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.createAnimal({
        name: form.name,
        species: form.species,
        breed: form.breed,
        client_id: Number(form.client_id),
        birth_date: form.birth_date || undefined,
        weight: form.weight ? Number(form.weight) : undefined,
      });
      toast("Animal cadastrado com sucesso!");
      setModalOpen(false);
      setForm({ name: "", species: "Cachorro", breed: "", birth_date: "", weight: "", client_id: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao cadastrar", "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header title="Animais" subtitle="Cadastro de pets e pacientes da clínica" />

      <div className="mb-6 flex flex-wrap items-center gap-4">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por nome ou espécie..."
            className="input-field pl-10"
          />
        </div>
        {isStaff && (
          <button onClick={() => setModalOpen(true)} className="btn-primary">
            <Plus size={18} /> Novo animal
          </button>
        )}
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : filtered.length === 0 ? (
        <div className="card"><EmptyState message="Nenhum animal encontrado" /></div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((a) => (
            <div key={a.id} className="card group transition hover:shadow-card-hover">
              <div className="flex items-start gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-clinic-100 text-2xl">
                  {getEmoji(a.species)}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-slate-900 truncate">{a.name}</h3>
                  <p className="text-sm text-slate-500">{a.species} · {a.breed}</p>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {a.weight && (
                      <span className="badge bg-slate-100 text-slate-600">{a.weight} kg</span>
                    )}
                    <span className="badge bg-clinic-100 text-clinic-700">Tutor #{a.client_id}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Cadastrar animal">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Nome</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Espécie</label>
              <select value={form.species} onChange={(e) => setForm({ ...form, species: e.target.value })} className="input-field">
                {["Cachorro", "Gato", "Ave", "Coelho", "Réptil", "Outro"].map((s) => (
                  <option key={s}>{s}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Raça</label>
              <input value={form.breed} onChange={(e) => setForm({ ...form, breed: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Peso (kg)</label>
              <input type="number" step="0.1" value={form.weight} onChange={(e) => setForm({ ...form, weight: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Nascimento</label>
              <input type="date" value={form.birth_date} onChange={(e) => setForm({ ...form, birth_date: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Tutor</label>
              <select value={form.client_id} onChange={(e) => setForm({ ...form, client_id: e.target.value })} className="input-field" required>
                <option value="">Selecione...</option>
                {clients.map((c) => (
                  <option key={c.id} value={c.id}>{c.nome_completo}</option>
                ))}
              </select>
            </div>
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
