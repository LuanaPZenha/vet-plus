import type {
  Client,
  Animal,
  MedicalHistoryEntry,
  Consultation,
  Veterinarian,
  Vaccine,
  UpcomingVaccine,
  Medicine,
  StockMovement,
} from "../types";

const TOKEN_KEY = "vetplus_token";
const USER_KEY = "vetplus_user";

const RENDER_DEFAULTS: Record<string, string> = {
  AUTH_URL: "https://vet-plus-auth.onrender.com",
  CLIENTS_URL: "https://vet-plus-clients.onrender.com",
  ANIMALS_URL: "https://vet-plus-animals.onrender.com",
  CONSULTATIONS_URL: "https://vet-plus-consultations.onrender.com",
  VACCINATION_URL: "https://vet-plus-vaccination.onrender.com",
  INVENTORY_URL: "https://vet-plus-inventory.onrender.com",
};

type ServiceUrlKey = Exclude<keyof VetPlusRuntimeEnv, "USE_API_PROXY">;

function useApiProxy(): boolean {
  const runtime = typeof window !== "undefined" ? window.__VET_PLUS_ENV__ : undefined;
  return runtime?.USE_API_PROXY === true;
}

function serviceBase(runtimeKey: ServiceUrlKey, viteKey: string): string {
  if (useApiProxy() || import.meta.env.DEV) return "";
  const runtime = typeof window !== "undefined" ? window.__VET_PLUS_ENV__ : undefined;
  return (
    runtime?.[runtimeKey] ??
    (import.meta.env[viteKey] as string | undefined) ??
    RENDER_DEFAULTS[runtimeKey] ??
    ""
  );
}

function apiUrl(base: string, path: string): string {
  if (!base) return path;
  return `${base.replace(/\/$/, "")}${path}`;
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function saveAuth(token: string, user: object) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  url: string,
  options: RequestInit = {},
  auth = true,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (auth) {
    const token = getToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg = data.error || data.detail || `Erro ${res.status}`;
    throw new ApiError(typeof msg === "string" ? msg : JSON.stringify(msg), res.status);
  }

  return data as T;
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string; user_id: number; email: string; role: string; full_name: string }>(
      apiUrl(serviceBase("AUTH_URL", "VITE_AUTH_URL"), "/api/login/"),
      { method: "POST", body: JSON.stringify({ email, password }) },
      false,
    ),

  register: (data: { email: string; password: string; full_name: string; role: string }) =>
    request(apiUrl(serviceBase("AUTH_URL", "VITE_AUTH_URL"), "/api/register/"), { method: "POST", body: JSON.stringify(data) }, false),

  getClients: () => request<Client[]>(apiUrl(serviceBase("CLIENTS_URL", "VITE_CLIENTS_URL"), "/api/clientes/")),
  createClient: (data: { nome_completo: string; email: string; telefone: string; cpf: string; endereco: string }) =>
    request<Client>(apiUrl(serviceBase("CLIENTS_URL", "VITE_CLIENTS_URL"), "/api/clientes/"), { method: "POST", body: JSON.stringify(data) }),

  getAnimals: () => request<Animal[]>(apiUrl(serviceBase("ANIMALS_URL", "VITE_ANIMALS_URL"), "/api/animais/")),
  createAnimal: (data: { name: string; species: string; breed: string; birth_date?: string; weight?: number; client_id: number }) =>
    request<Animal>(apiUrl(serviceBase("ANIMALS_URL", "VITE_ANIMALS_URL"), "/api/animais/"), { method: "POST", body: JSON.stringify(data) }),
  getAnimalHistory: (id: number) =>
    request<MedicalHistoryEntry[]>(apiUrl(serviceBase("ANIMALS_URL", "VITE_ANIMALS_URL"), `/api/animais/${id}/historico/`)),

  getConsultations: () => request<Consultation[]>(apiUrl(serviceBase("CONSULTATIONS_URL", "VITE_CONSULTATIONS_URL"), "/api/consultas/")),
  createConsultation: (data: { animal_id: number; veterinarian_id: number; scheduled_at: string; type: string; notes?: string }) =>
    request<Consultation>(apiUrl(serviceBase("CONSULTATIONS_URL", "VITE_CONSULTATIONS_URL"), "/api/consultas/"), { method: "POST", body: JSON.stringify(data) }),
  completeConsultation: (id: number, data: { diagnosis: string; prescription_notes?: string; procedure?: string }) =>
    request<Consultation>(apiUrl(serviceBase("CONSULTATIONS_URL", "VITE_CONSULTATIONS_URL"), `/api/consultas/${id}/concluir/`), { method: "PATCH", body: JSON.stringify(data) }),

  getVeterinarians: () => request<Veterinarian[]>(apiUrl(serviceBase("CONSULTATIONS_URL", "VITE_CONSULTATIONS_URL"), "/api/veterinarios/")),
  createVeterinarian: (data: { user_id: number; full_name: string; crmv: string; specialty: string }) =>
    request<Veterinarian>(apiUrl(serviceBase("CONSULTATIONS_URL", "VITE_CONSULTATIONS_URL"), "/api/veterinarios/"), { method: "POST", body: JSON.stringify(data) }),

  getVaccines: () => request<Vaccine[]>(apiUrl(serviceBase("VACCINATION_URL", "VITE_VACCINATION_URL"), "/api/vacinas/")),
  createVaccine: (data: {
    animal_id: number;
    vaccine_name: string;
    application_date: string;
    next_dose_date?: string;
    veterinarian_id: number;
    batch_number?: string;
    notes?: string;
  }) => request<Vaccine>(apiUrl(serviceBase("VACCINATION_URL", "VITE_VACCINATION_URL"), "/api/vacinas/"), { method: "POST", body: JSON.stringify(data) }),
  getUpcomingVaccines: () => request<UpcomingVaccine[]>(apiUrl(serviceBase("VACCINATION_URL", "VITE_VACCINATION_URL"), "/api/vacinas/proximas/")),

  getMedicines: () => request<Medicine[]>(apiUrl(serviceBase("INVENTORY_URL", "VITE_INVENTORY_URL"), "/api/medicamentos/")),
  createMedicine: (data: {
    name: string;
    generic_name?: string;
    category: string;
    unit: string;
    quantity: number;
    min_stock: number;
    batch_number?: string;
    expiration_date?: string;
    supplier?: string;
    unit_price?: number;
  }) => request<Medicine>(apiUrl(serviceBase("INVENTORY_URL", "VITE_INVENTORY_URL"), "/api/medicamentos/"), { method: "POST", body: JSON.stringify(data) }),
  stockEntry: (id: number, data: { quantity: number; reason: string }) =>
    request<StockMovement>(apiUrl(serviceBase("INVENTORY_URL", "VITE_INVENTORY_URL"), `/api/medicamentos/${id}/entrada/`), { method: "POST", body: JSON.stringify(data) }),
  stockExit: (id: number, data: { quantity: number; reason: string }) =>
    request<StockMovement>(apiUrl(serviceBase("INVENTORY_URL", "VITE_INVENTORY_URL"), `/api/medicamentos/${id}/saida/`), { method: "POST", body: JSON.stringify(data) }),
  getLowStock: () => request<Medicine[]>(apiUrl(serviceBase("INVENTORY_URL", "VITE_INVENTORY_URL"), "/api/medicamentos/baixo-estoque/")),
  getMovements: (medicineId?: number) => {
    const path = medicineId
      ? `/api/medicamentos/movimentacoes/?medicine_id=${medicineId}`
      : "/api/medicamentos/movimentacoes/";
    return request<StockMovement[]>(apiUrl(serviceBase("INVENTORY_URL", "VITE_INVENTORY_URL"), path));
  },
};
