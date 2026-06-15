import { useEffect, useState, type FormEvent } from "react";
import { Plus, Package, ArrowDownCircle, ArrowUpCircle, AlertTriangle } from "lucide-react";
import { Header } from "../components/Header";
import { Modal } from "../components/Modal";
import { LoadingSpinner, EmptyState } from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { api, ApiError } from "../api/client";
import type { Medicine } from "../types";

const categoryLabels: Record<string, string> = {
  antibiotico: "Antibiótico",
  analgesico: "Analgésico",
  anti_inflamatorio: "Anti-inflamatório",
  vacina: "Vacina",
  anestesico: "Anestésico",
  suplemento: "Suplemento",
  outro: "Outro",
};

export function InventoryPage() {
  const { isStaff } = useAuth();
  const { toast } = useToast();
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [lowStock, setLowStock] = useState<Medicine[]>([]);
  const [loading, setLoading] = useState(true);
  const [createModal, setCreateModal] = useState(false);
  const [movementModal, setMovementModal] = useState<{ med: Medicine; type: "entrada" | "saida" } | null>(null);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    name: "", generic_name: "", category: "antibiotico", unit: "un",
    quantity: "", min_stock: "10", batch_number: "", expiration_date: "", supplier: "", unit_price: "",
  });
  const [movementForm, setMovementForm] = useState({ quantity: "", reason: "" });

  const load = () => {
    setLoading(true);
    Promise.all([api.getMedicines(), api.getLowStock()])
      .then(([m, l]) => { setMedicines(m); setLowStock(l); })
      .catch(() => toast("Erro ao carregar estoque", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.createMedicine({
        name: form.name,
        generic_name: form.generic_name,
        category: form.category,
        unit: form.unit,
        quantity: Number(form.quantity),
        min_stock: Number(form.min_stock),
        batch_number: form.batch_number || undefined,
        expiration_date: form.expiration_date || undefined,
        supplier: form.supplier || undefined,
        unit_price: form.unit_price ? Number(form.unit_price) : undefined,
      });
      toast("Medicamento cadastrado!");
      setCreateModal(false);
      setForm({ name: "", generic_name: "", category: "antibiotico", unit: "un", quantity: "", min_stock: "10", batch_number: "", expiration_date: "", supplier: "", unit_price: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao cadastrar", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleMovement = async (e: FormEvent) => {
    e.preventDefault();
    if (!movementModal) return;
    setSaving(true);
    try {
      const data = { quantity: Number(movementForm.quantity), reason: movementForm.reason };
      if (movementModal.type === "entrada") {
        await api.stockEntry(movementModal.med.id, data);
        toast("Entrada registrada!");
      } else {
        await api.stockExit(movementModal.med.id, data);
        toast("Saída registrada!");
      }
      setMovementModal(null);
      setMovementForm({ quantity: "", reason: "" });
      load();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro na movimentação", "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header title="Estoque" subtitle="Controle de medicamentos e insumos veterinários" />

      {lowStock.length > 0 && (
        <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4">
          <div className="flex items-center gap-2 text-red-800">
            <AlertTriangle size={20} />
            <span className="font-semibold">{lowStock.length} medicamento(s) com estoque baixo</span>
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {lowStock.map((m) => (
              <span key={m.id} className="badge bg-red-100 text-red-700">
                {m.name}: {m.quantity} {m.unit} (mín. {m.min_stock})
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mb-6 flex justify-end">
        {isStaff && (
          <button onClick={() => setCreateModal(true)} className="btn-primary">
            <Plus size={18} /> Novo medicamento
          </button>
        )}
      </div>

      <div className="card overflow-hidden !p-0">
        {loading ? (
          <LoadingSpinner />
        ) : medicines.length === 0 ? (
          <EmptyState message="Nenhum medicamento no estoque" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/80 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <th className="px-6 py-3">Medicamento</th>
                  <th className="px-6 py-3">Categoria</th>
                  <th className="px-6 py-3">Quantidade</th>
                  <th className="px-6 py-3">Validade</th>
                  <th className="px-6 py-3">Status</th>
                  {isStaff && <th className="px-6 py-3">Ações</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {medicines.map((m) => (
                  <tr key={m.id} className="hover:bg-clinic-50/50">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-clinic-100">
                          <Package size={18} className="text-clinic-600" />
                        </div>
                        <div>
                          <p className="font-medium text-slate-800">{m.name}</p>
                          {m.generic_name && <p className="text-xs text-slate-400">{m.generic_name}</p>}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-600">{categoryLabels[m.category] || m.category}</td>
                    <td className="px-6 py-4">
                      <span className={`font-semibold ${m.is_low_stock ? "text-red-600" : "text-slate-800"}`}>
                        {m.quantity} {m.unit}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-slate-600">
                      {m.expiration_date ? new Date(m.expiration_date).toLocaleDateString("pt-BR") : "—"}
                    </td>
                    <td className="px-6 py-4">
                      {m.is_expired ? (
                        <span className="badge bg-red-100 text-red-700">Vencido</span>
                      ) : m.is_low_stock ? (
                        <span className="badge bg-amber-100 text-amber-700">Baixo</span>
                      ) : (
                        <span className="badge bg-clinic-100 text-clinic-700">OK</span>
                      )}
                    </td>
                    {isStaff && (
                      <td className="px-6 py-4">
                        <div className="flex gap-2">
                          <button
                            onClick={() => { setMovementModal({ med: m, type: "entrada" }); setMovementForm({ quantity: "", reason: "" }); }}
                            className="flex items-center gap-1 text-xs font-medium text-pet-500 hover:text-pet-600"
                          >
                            <ArrowDownCircle size={16} /> Entrada
                          </button>
                          <button
                            onClick={() => { setMovementModal({ med: m, type: "saida" }); setMovementForm({ quantity: "", reason: "" }); }}
                            className="flex items-center gap-1 text-xs font-medium text-orange-600 hover:text-orange-700"
                          >
                            <ArrowUpCircle size={16} /> Saída
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={createModal} onClose={() => setCreateModal(false)} title="Cadastrar medicamento" wide>
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Nome comercial</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Princípio ativo</label>
              <input value={form.generic_name} onChange={(e) => setForm({ ...form, generic_name: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Categoria</label>
              <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className="input-field">
                {Object.entries(categoryLabels).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Unidade</label>
              <select value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} className="input-field">
                {["un", "ml", "comp", "fr", "amp", "kg"].map((u) => <option key={u}>{u}</option>)}
              </select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Quantidade inicial</label>
              <input type="number" step="0.01" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Estoque mínimo</label>
              <input type="number" step="0.01" value={form.min_stock} onChange={(e) => setForm({ ...form, min_stock: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Lote</label>
              <input value={form.batch_number} onChange={(e) => setForm({ ...form, batch_number: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Validade</label>
              <input type="date" value={form.expiration_date} onChange={(e) => setForm({ ...form, expiration_date: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Fornecedor</label>
              <input value={form.supplier} onChange={(e) => setForm({ ...form, supplier: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Preço unitário (R$)</label>
              <input type="number" step="0.01" value={form.unit_price} onChange={(e) => setForm({ ...form, unit_price: e.target.value })} className="input-field" />
            </div>
          </div>
          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => setCreateModal(false)} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-primary">{saving ? "Salvando..." : "Cadastrar"}</button>
          </div>
        </form>
      </Modal>

      <Modal
        open={!!movementModal}
        onClose={() => setMovementModal(null)}
        title={movementModal?.type === "entrada" ? "Entrada de estoque" : "Saída de estoque"}
      >
        {movementModal && (
          <form onSubmit={handleMovement} className="space-y-4">
            <p className="text-sm text-slate-600">
              <strong>{movementModal.med.name}</strong> — Estoque atual: {movementModal.med.quantity} {movementModal.med.unit}
            </p>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Quantidade</label>
              <input type="number" step="0.01" value={movementForm.quantity} onChange={(e) => setMovementForm({ ...movementForm, quantity: e.target.value })} className="input-field" required />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Motivo</label>
              <textarea value={movementForm.reason} onChange={(e) => setMovementForm({ ...movementForm, reason: e.target.value })} className="input-field" rows={2} required placeholder={movementModal.type === "entrada" ? "Ex: Compra fornecedor XYZ" : "Ex: Prescrição consulta #12"} />
            </div>
            <div className="flex justify-end gap-3">
              <button type="button" onClick={() => setMovementModal(null)} className="btn-secondary">Cancelar</button>
              <button type="submit" disabled={saving} className="btn-primary">{saving ? "Registrando..." : "Confirmar"}</button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}
