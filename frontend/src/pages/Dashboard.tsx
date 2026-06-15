import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Users, PawPrint, CalendarClock, Syringe, Package, ArrowRight } from "lucide-react";
import { Header } from "../components/Header";
import { StatCard } from "../components/StatCard";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { api } from "../api/client";
import type { Consultation, UpcomingVaccine } from "../types";

const statusLabels: Record<string, { label: string; class: string }> = {
  scheduled: { label: "Agendada", class: "bg-vet-100 text-vet-700" },
  in_progress: { label: "Em andamento", class: "bg-honey-400/25 text-amber-800" },
  completed: { label: "Concluída", class: "bg-accent-500/15 text-accent-600" },
  cancelled: { label: "Cancelada", class: "bg-vet-100/80 text-vet-500" },
};

const typeLabels: Record<string, string> = {
  regular: "Consulta",
  emergency: "Emergência",
  surgery: "Cirurgia",
};

export function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ clients: 0, animals: 0, consultations: 0, vaccines: 0, medicines: 0, lowStock: 0 });
  const [recentConsultations, setRecentConsultations] = useState<Consultation[]>([]);
  const [upcomingVaccines, setUpcomingVaccines] = useState<UpcomingVaccine[]>([]);

  useEffect(() => {
    Promise.all([
      api.getClients().catch(() => []),
      api.getAnimals().catch(() => []),
      api.getConsultations().catch(() => []),
      api.getVaccines().catch(() => []),
      api.getUpcomingVaccines().catch(() => []),
      api.getMedicines().catch(() => []),
      api.getLowStock().catch(() => []),
    ]).then(([clients, animals, consultations, vaccines, upcoming, medicines, lowStock]) => {
      setStats({
        clients: clients.length,
        animals: animals.length,
        consultations: consultations.filter((c) => c.status === "scheduled").length,
        vaccines: vaccines.length,
        medicines: medicines.length,
        lowStock: lowStock.length,
      });
      setRecentConsultations(
        consultations
          .sort((a, b) => new Date(b.scheduled_at).getTime() - new Date(a.scheduled_at).getTime())
          .slice(0, 5),
      );
      setUpcomingVaccines(upcoming.slice(0, 5));
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner label="Carregando dashboard..." />;

  return (
    <div>
      <Header title="Dashboard" subtitle="Visão geral da clínica veterinária" />

      <div className="mb-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        <StatCard title="Tutores cadastrados" value={stats.clients} icon={Users} color="vet" />
        <StatCard title="Animais ativos" value={stats.animals} icon={PawPrint} color="accent" />
        <StatCard title="Consultas agendadas" value={stats.consultations} icon={CalendarClock} color="honey" />
        <StatCard title="Vacinas registradas" value={stats.vaccines} icon={Syringe} color="rose" />
        <StatCard title="Medicamentos em estoque" value={stats.medicines} icon={Package} color="vet" trend={stats.lowStock > 0 ? `${stats.lowStock} com estoque baixo` : undefined} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="font-semibold text-vet-900">Consultas recentes</h3>
            <Link to="/consultas" className="flex items-center gap-1 text-sm font-medium text-accent-600 hover:text-accent-500">
              Ver todas <ArrowRight size={16} />
            </Link>
          </div>
          {recentConsultations.length === 0 ? (
            <p className="py-8 text-center text-sm text-vet-400">Nenhuma consulta registrada</p>
          ) : (
            <div className="space-y-3">
              {recentConsultations.map((c) => {
                const st = statusLabels[c.status] || statusLabels.scheduled;
                return (
                  <div key={c.id} className="flex items-center justify-between rounded-lg bg-warm-200/80 px-4 py-3">
                    <div>
                      <p className="text-sm font-medium text-vet-900">
                        Animal #{c.animal_id} — {typeLabels[c.type] || c.type}
                      </p>
                      <p className="text-xs text-vet-500">
                        {new Date(c.scheduled_at).toLocaleString("pt-BR")}
                      </p>
                    </div>
                    <span className={`badge ${st.class}`}>{st.label}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="font-semibold text-vet-900">Vacinas próximas do vencimento</h3>
            <Link to="/vacinas" className="flex items-center gap-1 text-sm font-medium text-accent-600 hover:text-accent-500">
              Ver todas <ArrowRight size={16} />
            </Link>
          </div>
          {upcomingVaccines.length === 0 ? (
            <p className="py-8 text-center text-sm text-vet-400">Nenhuma vacina próxima do vencimento</p>
          ) : (
            <div className="space-y-3">
              {upcomingVaccines.map((v) => (
                <div key={v.id} className="flex items-center justify-between rounded-lg bg-honey-400/15 px-4 py-3">
                  <div>
                    <p className="text-sm font-medium text-vet-900">{v.vaccine_name}</p>
                    <p className="text-xs text-vet-500">Animal #{v.animal_id}</p>
                  </div>
                  <span className="badge bg-honey-400/30 text-amber-800">
                    {v.days_until_due <= 0 ? "Vencida" : `${v.days_until_due} dias`}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
