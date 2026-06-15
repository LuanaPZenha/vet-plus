import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ToastProvider } from "./context/ToastContext";
import { Layout } from "./components/Layout";
import { LoginPage } from "./pages/Login";
import { DashboardPage } from "./pages/Dashboard";
import { ClientsPage } from "./pages/Clients";
import { AnimalsPage } from "./pages/Animals";
import { ConsultationsPage } from "./pages/Consultations";
import { VaccinesPage } from "./pages/Vaccines";
import { InventoryPage } from "./pages/Inventory";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<Layout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/clientes" element={<ClientsPage />} />
              <Route path="/animais" element={<AnimalsPage />} />
              <Route path="/consultas" element={<ConsultationsPage />} />
              <Route path="/vacinas" element={<VaccinesPage />} />
              <Route path="/estoque" element={<InventoryPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
