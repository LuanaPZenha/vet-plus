import { useState, type FormEvent } from "react";
import { Navigate } from "react-router-dom";
import { Heart, Mail, Lock, Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { ApiError } from "../api/client";

export function LoginPage() {
  const { user, login } = useAuth();
  const { toast } = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      toast("Login realizado com sucesso!");
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Erro ao fazer login", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      <div className="hidden w-1/2 flex-col justify-between bg-gradient-to-br from-vet-700 via-vet-800 to-[#2a1845] p-12 text-warm-50 lg:flex">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-accent-500/30 ring-2 ring-honey-400/50">
            <Heart size={24} className="text-honey-400" fill="currentColor" />
          </div>
          <span className="text-2xl font-bold">Vet Plus+</span>
        </div>

        <div>
          <h2 className="text-4xl font-bold leading-tight">
            Cuidado completo<br />para seus pacientes
          </h2>
          <p className="mt-4 max-w-md text-lg text-vet-200">
            Gerencie tutores, animais, consultas e vacinas em um só lugar — simples, rápido e profissional.
          </p>

          <div className="mt-10 grid grid-cols-3 gap-4">
            {[
              { n: "5", l: "Módulos" },
              { n: "24/7", l: "Disponível" },
              { n: "100%", l: "Seguro" },
            ].map((s) => (
              <div key={s.l} className="rounded-xl bg-vet-600/40 p-4 text-center ring-1 ring-vet-500/30">
                <p className="text-2xl font-bold text-honey-400">{s.n}</p>
                <p className="text-xs text-vet-200">{s.l}</p>
              </div>
            ))}
          </div>
        </div>

        <p className="text-sm text-vet-300">© 2024 Vet Plus+ — Engenharia de Software</p>
      </div>

      <div className="flex flex-1 items-center justify-center bg-warm-100 p-8">
        <div className="w-full max-w-md">
          <div className="mb-8 lg:hidden">
            <div className="flex items-center gap-2 text-vet-700">
              <Heart size={28} className="text-accent-500" fill="currentColor" />
              <span className="text-xl font-bold">Vet Plus+</span>
            </div>
          </div>

          <h1 className="text-2xl font-bold text-vet-900">Entrar no sistema</h1>
          <p className="mt-2 text-sm text-vet-500">Acesse o painel da clínica veterinária</p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-vet-700">E-mail</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 text-vet-400" size={18} />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field pl-10"
                  placeholder="seu@email.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium text-vet-700">Senha</label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-vet-400" size={18} />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field pl-10"
                  placeholder="••••••••"
                  required
                  minLength={8}
                />
              </div>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full py-3">
              {loading ? <Loader2 className="animate-spin" size={20} /> : "Entrar"}
            </button>
          </form>

          <p className="mt-6 text-center text-xs text-vet-400">
            Demo: admin@vet.com / senha1234
          </p>
        </div>
      </div>
    </div>
  );
}
