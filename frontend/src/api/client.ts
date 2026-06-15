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
      "/api/login/",
      { method: "POST", body: JSON.stringify({ email, password }) },
      false,
    ),

  register: (data: { email: string; password: string; full_name: string; role: string }) =>
    request("/api/register/", { method: "POST", body: JSON.stringify(data) }, false),

  getClients: () => request<Client[]>("/api/clientes/"),
  createClient: (data: { nome_completo: string; email: string; telefone: string; cpf: string; endereco: string }) =>
    request<Client>("/api/clientes/", { method: "POST", body: JSON.stringify(data) }),

  getAnimals: () => request<Animal[]>("/api/animais/"),
  createAnimal: (data: { name: string; species: string; breed: string; birth_date?: string; weight?: number; client_id: number }) =>
    request<Animal>("/api/animais/", { method: "POST", body: JSON.stringify(data) }),
  getAnimalHistory: (id: number) =>
    request<MedicalHistoryEntry[]>(`/api/animais/${id}/historico/`),

  getConsultations: () => request<Consultation[]>("/api/consultas/"),
  createConsultation: (data: { animal_id: number; veterinarian_id: number; scheduled_at: string; type: string; notes?: string }) =>
    request<Consultation>("/api/consultas/", { method: "POST", body: JSON.stringify(data) }),
  completeConsultation: (id: number, data: { diagnosis: string; prescription_notes?: string; procedure?: string }) =>
    request<Consultation>(`/api/consultas/${id}/concluir/`, { method: "PATCH", body: JSON.stringify(data) }),

  getVeterinarians: () => request<Veterinarian[]>("/api/veterinarios/"),
  createVeterinarian: (data: { user_id: number; full_name: string; crmv: string; specialty: string }) =>
    request<Veterinarian>("/api/veterinarios/", { method: "POST", body: JSON.stringify(data) }),

  getVaccines: () => request<Vaccine[]>("/api/vacinas/"),
  createVaccine: (data: {
    animal_id: number;
    vaccine_name: string;
    application_date: string;
    next_dose_date?: string;
    veterinarian_id: number;
    batch_number?: string;
    notes?: string;
  }) => request<Vaccine>("/api/vacinas/", { method: "POST", body: JSON.stringify(data) }),
  getUpcomingVaccines: () => request<UpcomingVaccine[]>("/api/vacinas/proximas/"),

  getMedicines: () => request<Medicine[]>("/api/medicamentos/"),
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
  }) => request<Medicine>("/api/medicamentos/", { method: "POST", body: JSON.stringify(data) }),
  stockEntry: (id: number, data: { quantity: number; reason: string }) =>
    request<StockMovement>(`/api/medicamentos/${id}/entrada/`, { method: "POST", body: JSON.stringify(data) }),
  stockExit: (id: number, data: { quantity: number; reason: string }) =>
    request<StockMovement>(`/api/medicamentos/${id}/saida/`, { method: "POST", body: JSON.stringify(data) }),
  getLowStock: () => request<Medicine[]>("/api/medicamentos/baixo-estoque/"),
  getMovements: (medicineId?: number) => {
    const url = medicineId
      ? `/api/medicamentos/movimentacoes/?medicine_id=${medicineId}`
      : "/api/medicamentos/movimentacoes/";
    return request<StockMovement[]>(url);
  },
};
