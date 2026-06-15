import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  PawPrint,
  CalendarClock,
  Syringe,
  Package,
  LogOut,
  Heart,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const navItems = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/clientes", icon: Users, label: "Tutores" },
  { to: "/animais", icon: PawPrint, label: "Animais" },
  { to: "/consultas", icon: CalendarClock, label: "Consultas" },
  { to: "/vacinas", icon: Syringe, label: "Vacinas" },
  { to: "/estoque", icon: Package, label: "Estoque" },
];

export function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside className="fixed inset-y-0 left-0 z-30 flex w-64 flex-col bg-gradient-to-b from-vet-800 via-vet-900 to-[#2a1845] text-warm-50">
      <div className="flex items-center gap-3 border-b border-vet-600/40 px-6 py-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent-500/30 ring-2 ring-honey-400/40">
          <Heart className="h-5 w-5 text-honey-400" fill="currentColor" />
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight">Vet+ Clinic</h1>
          <p className="text-xs text-vet-200">Gestão Veterinária</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                isActive
                  ? "bg-accent-500 text-white shadow-md shadow-accent-500/30"
                  : "text-vet-100 hover:bg-vet-700/60 hover:text-warm-50"
              }`
            }
          >
            <Icon size={20} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-vet-600/40 p-4">
        <div className="mb-3 rounded-lg bg-vet-700/50 px-3 py-2.5">
          <p className="truncate text-sm font-medium">{user?.full_name}</p>
          <p className="truncate text-xs capitalize text-vet-200">{user?.role}</p>
        </div>
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-vet-100 transition hover:bg-vet-700/60 hover:text-warm-50"
        >
          <LogOut size={18} />
          Sair
        </button>
      </div>
    </aside>
  );
}
