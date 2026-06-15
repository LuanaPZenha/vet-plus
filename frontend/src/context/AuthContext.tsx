import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { api, saveAuth, clearAuth, getStoredUser, getToken } from "../api/client";
import type { AuthUser } from "../types";

interface AuthContextType {
  user: AuthUser | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isStaff: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => {
    const stored = getStoredUser();
    const token = getToken();
    if (stored && token) {
      return { ...stored, access_token: token } as AuthUser;
    }
    return null;
  });

  const login = useCallback(async (email: string, password: string) => {
    const res = await api.login(email, password);
    const authUser: AuthUser = {
      user_id: res.user_id,
      email: res.email,
      role: res.role as AuthUser["role"],
      full_name: res.full_name,
      access_token: res.access_token,
    };
    saveAuth(res.access_token, {
      user_id: res.user_id,
      email: res.email,
      role: res.role,
      full_name: res.full_name,
    });
    setUser(authUser);
  }, []);

  const logout = useCallback(() => {
    clearAuth();
    setUser(null);
  }, []);

  const isStaff = user?.role === "admin" || user?.role === "veterinarian";

  return (
    <AuthContext.Provider value={{ user, login, logout, isStaff }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
