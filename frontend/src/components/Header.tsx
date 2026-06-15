import { Bell } from "lucide-react";
import { useAuth } from "../context/AuthContext";

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  const { user } = useAuth();
  const greeting = getGreeting();

  return (
    <header className="mb-8 flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-accent-600">{greeting}, {user?.full_name?.split(" ")[0]}</p>
        <h2 className="text-2xl font-bold text-vet-900">{title}</h2>
        {subtitle && <p className="mt-1 text-sm text-vet-500">{subtitle}</p>}
      </div>
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-vet-100 text-vet-600 ring-2 ring-accent-200">
        <Bell size={18} />
      </div>
    </header>
  );
}

function getGreeting() {
  const h = new Date().getHours();
  if (h < 12) return "Bom dia";
  if (h < 18) return "Boa tarde";
  return "Boa noite";
}
