export interface AuthUser {
  user_id: number;
  email: string;
  role: "admin" | "veterinarian" | "tutor";
  full_name: string;
  access_token: string;
}

export interface Client {
  id: number;
  nome_completo: string;
  email: string;
  telefone: string;
  cpf: string;
  endereco: string;
  criado_em: string;
}

export interface Animal {
  id: number;
  name: string;
  species: string;
  breed: string;
  birth_date: string | null;
  weight: string | null;
  client_id: number;
  created_at: string;
}

export interface Consultation {
  id: number;
  animal_id: number;
  veterinarian_id: number;
  scheduled_at: string;
  status: string;
  type: string;
  price: string | null;
  notes: string;
  diagnosis: string;
  prescription: string;
  created_at: string;
}

export interface Veterinarian {
  id: number;
  user_id: number;
  full_name: string;
  crmv: string;
  specialty: string;
  created_at: string;
}

export interface Vaccine {
  id: number;
  animal_id: number;
  vaccine_name: string;
  application_date: string;
  next_dose_date: string | null;
  veterinarian_id: number;
  batch_number: string | null;
  notes: string | null;
  created_at: string;
}

export interface UpcomingVaccine {
  id: number;
  animal_id: number;
  vaccine_name: string;
  next_dose_date: string;
  days_until_due: number;
}

export interface Medicine {
  id: number;
  name: string;
  generic_name: string;
  category: string;
  unit: string;
  quantity: string;
  min_stock: string;
  batch_number: string | null;
  expiration_date: string | null;
  supplier: string | null;
  unit_price: string | null;
  is_low_stock: boolean;
  is_expired: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface StockMovement {
  id: number;
  medicine_id: number;
  movement_type: string;
  quantity: string;
  reason: string;
  performed_by: number;
  stock_after: string;
  created_at: string | null;
}

export interface MedicalHistoryEntry {
  id: number;
  animal_id: number;
  description: string;
  record_type: string;
  created_at: string;
}
