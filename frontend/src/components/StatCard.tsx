import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  color: "teal" | "blue" | "amber" | "rose";
  trend?: string;
}

const colors = {
  teal: { bg: "bg-clinic-100", text: "text-clinic-600", icon: "text-clinic-600" },
  blue: { bg: "bg-blue-100", text: "text-blue-600", icon: "text-blue-600" },
  amber: { bg: "bg-amber-100", text: "text-amber-600", icon: "text-amber-600" },
  rose: { bg: "bg-rose-100", text: "text-rose-600", icon: "text-rose-600" },
};

export function StatCard({ title, value, icon: Icon, color, trend }: StatCardProps) {
  const c = colors[color];
  return (
    <div className="card group transition hover:shadow-card-hover">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className={`mt-2 text-3xl font-bold ${c.text}`}>{value}</p>
          {trend && <p className="mt-1 text-xs text-slate-400">{trend}</p>}
        </div>
        <div className={`rounded-xl ${c.bg} p-3 transition group-hover:scale-105`}>
          <Icon className={c.icon} size={24} />
        </div>
      </div>
    </div>
  );
}
