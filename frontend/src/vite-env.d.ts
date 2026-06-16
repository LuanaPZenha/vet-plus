/// <reference types="vite/client" />

interface VetPlusRuntimeEnv {
  AUTH_URL?: string;
  CLIENTS_URL?: string;
  ANIMALS_URL?: string;
  CONSULTATIONS_URL?: string;
  VACCINATION_URL?: string;
  INVENTORY_URL?: string;
}

interface Window {
  __VET_PLUS_ENV__?: VetPlusRuntimeEnv;
}
