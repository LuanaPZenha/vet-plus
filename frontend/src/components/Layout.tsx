import { Outlet, Navigate } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { useAuth } from "../context/AuthContext";

export function Layout() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="min-h-screen">
      <Sidebar />
      <main className="ml-64 min-h-screen p-8">
        <Outlet />
      </main>
    </div>
  );
}
