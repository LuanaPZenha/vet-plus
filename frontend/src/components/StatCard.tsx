import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  color: "vet" | "accent" | "honey" | "rose";
  trend?: string;
}

const colors = {
  vet: { bg: "bg-vet-100", text: "text-vet-700", icon: "text-vet-600" },
  accent: { bg: "bg-accent-500/15", text: "text-accent-600", icon: "text-accent-500" },
  honey: { bg: "bg-honey-400/20", text: "text-amber-700", icon: "text-honey-500" },
  rose: { bg: "bg-rose-100", text: "text-rose-600", icon: "text-rose-600" },
};

export function StatCard({ title, value, icon: Icon, color, trend }: StatCardProps) {
  const c = colors[color];
  return (
    <div className="card group transition hover:shadow-card-hover">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-vet-500">{title}</p>
          <p className={`mt-2 text-3xl font-bold ${c.text}`}>{value}</p>
          {trend && <p className="mt-1 text-xs text-vet-400">{trend}</p>}
        </div>
        <div className={`rounded-xl ${c.bg} p-3 transition group-hover:scale-105`}>
          <Icon className={c.icon} size={24} />
        </div>
      </div>
    </div>
  );
}
