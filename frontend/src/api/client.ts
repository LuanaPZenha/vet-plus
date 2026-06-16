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

const AUTH_BASE = import.meta.env.VITE_AUTH_URL ?? "";
const CLIENTS_BASE = import.meta.env.VITE_CLIENTS_URL ?? "";
const ANIMALS_BASE = import.meta.env.VITE_ANIMALS_URL ?? "";
const CONSULTATIONS_BASE = import.meta.env.VITE_CONSULTATIONS_URL ?? "";
const VACCINATION_BASE = import.meta.env.VITE_VACCINATION_URL ?? "";
const INVENTORY_BASE = import.meta.env.VITE_INVENTORY_URL ?? "";

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
      apiUrl(AUTH_BASE, "/api/login/"),
      { method: "POST", body: JSON.stringify({ email, password }) },
      false,
    ),

  register: (data: { email: string; password: string; full_name: string; role: string }) =>
    request(apiUrl(AUTH_BASE, "/api/register/"), { method: "POST", body: JSON.stringify(data) }, false),

  getClients: () => request<Client[]>(apiUrl(CLIENTS_BASE, "/api/clientes/")),
  createClient: (data: { nome_completo: string; email: string; telefone: string; cpf: string; endereco: string }) =>
    request<Client>(apiUrl(CLIENTS_BASE, "/api/clientes/"), { method: "POST", body: JSON.stringify(data) }),

  getAnimals: () => request<Animal[]>(apiUrl(ANIMALS_BASE, "/api/animais/")),
  createAnimal: (data: { name: string; species: string; breed: string; birth_date?: string; weight?: number; client_id: number }) =>
    request<Animal>(apiUrl(ANIMALS_BASE, "/api/animais/"), { method: "POST", body: JSON.stringify(data) }),
  getAnimalHistory: (id: number) =>
    request<MedicalHistoryEntry[]>(apiUrl(ANIMALS_BASE, `/api/animais/${id}/historico/`)),

  getConsultations: () => request<Consultation[]>(apiUrl(CONSULTATIONS_BASE, "/api/consultas/")),
  createConsultation: (data: { animal_id: number; veterinarian_id: number; scheduled_at: string; type: string; notes?: string }) =>
    request<Consultation>(apiUrl(CONSULTATIONS_BASE, "/api/consultas/"), { method: "POST", body: JSON.stringify(data) }),
  completeConsultation: (id: number, data: { diagnosis: string; prescription_notes?: string; procedure?: string }) =>
    request<Consultation>(apiUrl(CONSULTATIONS_BASE, `/api/consultas/${id}/concluir/`), { method: "PATCH", body: JSON.stringify(data) }),

  getVeterinarians: () => request<Veterinarian[]>(apiUrl(CONSULTATIONS_BASE, "/api/veterinarios/")),
  createVeterinarian: (data: { user_id: number; full_name: string; crmv: string; specialty: string }) =>
    request<Veterinarian>(apiUrl(CONSULTATIONS_BASE, "/api/veterinarios/"), { method: "POST", body: JSON.stringify(data) }),

  getVaccines: () => request<Vaccine[]>(apiUrl(VACCINATION_BASE, "/api/vacinas/")),
  createVaccine: (data: {
    animal_id: number;
    vaccine_name: string;
    application_date: string;
    next_dose_date?: string;
    veterinarian_id: number;
    batch_number?: string;
    notes?: string;
  }) => request<Vaccine>(apiUrl(VACCINATION_BASE, "/api/vacinas/"), { method: "POST", body: JSON.stringify(data) }),
  getUpcomingVaccines: () => request<UpcomingVaccine[]>(apiUrl(VACCINATION_BASE, "/api/vacinas/proximas/")),

  getMedicines: () => request<Medicine[]>(apiUrl(INVENTORY_BASE, "/api/medicamentos/")),
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
  }) => request<Medicine>(apiUrl(INVENTORY_BASE, "/api/medicamentos/"), { method: "POST", body: JSON.stringify(data) }),
  stockEntry: (id: number, data: { quantity: number; reason: string }) =>
    request<StockMovement>(apiUrl(INVENTORY_BASE, `/api/medicamentos/${id}/entrada/`), { method: "POST", body: JSON.stringify(data) }),
  stockExit: (id: number, data: { quantity: number; reason: string }) =>
    request<StockMovement>(apiUrl(INVENTORY_BASE, `/api/medicamentos/${id}/saida/`), { method: "POST", body: JSON.stringify(data) }),
  getLowStock: () => request<Medicine[]>(apiUrl(INVENTORY_BASE, "/api/medicamentos/baixo-estoque/")),
  getMovements: (medicineId?: number) => {
    const path = medicineId
      ? `/api/medicamentos/movimentacoes/?medicine_id=${medicineId}`
      : "/api/medicamentos/movimentacoes/";
    return request<StockMovement[]>(apiUrl(INVENTORY_BASE, path));
  },
};
