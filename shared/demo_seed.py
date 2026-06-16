"""Dados de demonstração compartilhados entre microsserviços Vet Plus+."""

from __future__ import annotations

DEMO_USERS = [
    {
        "email": "admin@vet.com",
        "password": "senha1234",
        "full_name": "Admin Demo",
        "role": "admin",
        "is_staff": True,
    },
    {
        "email": "dr.silva@vet.com",
        "password": "senha1234",
        "full_name": "Dra. Marina Silva",
        "role": "veterinarian",
        "is_staff": False,
    },
    {
        "email": "dr.costa@vet.com",
        "password": "senha1234",
        "full_name": "Dr. Paulo Costa",
        "role": "veterinarian",
        "is_staff": False,
    },
]

DEMO_CLIENTS = [
    {
        "full_name": "Maria Souza",
        "email": "maria.souza@email.com",
        "phone": "11987654321",
        "cpf": "123.456.789-01",
        "address": "Rua das Palmeiras, 120 - São Paulo, SP",
    },
    {
        "full_name": "Carlos Lima",
        "email": "carlos.lima@email.com",
        "phone": "11976543210",
        "cpf": "234.567.890-12",
        "address": "Av. Brasil, 450 - Campinas, SP",
    },
    {
        "full_name": "Ana Costa",
        "email": "ana.costa@email.com",
        "phone": "11965432109",
        "cpf": "345.678.901-23",
        "address": "Rua Ipê, 78 - Santos, SP",
    },
]

DEMO_ANIMALS = [
    {
        "name": "Rex",
        "species": "Cão",
        "breed": "Labrador Retriever",
        "birth_date": "2020-05-10",
        "weight": "28.50",
        "client_email": "maria.souza@email.com",
    },
    {
        "name": "Mimi",
        "species": "Gato",
        "breed": "Siamês",
        "birth_date": "2021-03-15",
        "weight": "4.20",
        "client_email": "carlos.lima@email.com",
    },
    {
        "name": "Thor",
        "species": "Cão",
        "breed": "Pastor Alemão",
        "birth_date": "2019-11-01",
        "weight": "35.00",
        "client_email": "ana.costa@email.com",
    },
]

DEMO_VETERINARIANS = [
    {
        "user_email": "admin@vet.com",
        "user_id": 1,
        "full_name": "Dr. Admin Vet",
        "crmv": "SP-10001",
        "specialty": "Clínica Geral",
    },
    {
        "user_email": "dr.silva@vet.com",
        "user_id": 2,
        "full_name": "Dra. Marina Silva",
        "crmv": "SP-10002",
        "specialty": "Dermatologia",
    },
    {
        "user_email": "dr.costa@vet.com",
        "user_id": 3,
        "full_name": "Dr. Paulo Costa",
        "crmv": "SP-10003",
        "specialty": "Cirurgia",
    },
]

DEMO_CONSULTATIONS = [
    {
        "animal_name": "Rex",
        "veterinarian_crmv": "SP-10001",
        "scheduled_at": "2026-06-20T10:00:00",
        "type": "regular",
        "notes": "Check-up anual e avaliação nutricional",
    },
    {
        "animal_name": "Mimi",
        "veterinarian_crmv": "SP-10002",
        "scheduled_at": "2026-06-21T14:30:00",
        "type": "emergency",
        "notes": "Vômito recorrente nas últimas 24 horas",
    },
    {
        "animal_name": "Thor",
        "veterinarian_crmv": "SP-10003",
        "scheduled_at": "2026-06-22T09:00:00",
        "type": "surgery",
        "notes": "Castração eletiva com exames pré-operatórios",
    },
]

DEMO_VACCINES = [
    {
        "animal_name": "Rex",
        "vaccine_name": "V10 (Polivalente)",
        "application_date": "2026-01-10",
        "next_dose_date": "2026-07-10",
        "veterinarian_crmv": "SP-10001",
        "batch_number": "VAC-2026-001",
        "notes": "Primeira dose do protocolo anual",
    },
    {
        "animal_name": "Mimi",
        "vaccine_name": "Antirrábica",
        "application_date": "2026-02-15",
        "next_dose_date": "2027-02-15",
        "veterinarian_crmv": "SP-10002",
        "batch_number": "VAC-2026-002",
        "notes": "Reforço anual obrigatório",
    },
    {
        "animal_name": "Thor",
        "vaccine_name": "Giardia",
        "application_date": "2026-03-01",
        "next_dose_date": "2026-09-01",
        "veterinarian_crmv": "SP-10003",
        "batch_number": "VAC-2026-003",
        "notes": "Protocolo filhote — segunda dose",
    },
]

DEMO_MEDICINES = [
    {
        "name": "Amoxicilina 500mg",
        "generic_name": "Amoxicilina",
        "category": "antibiotico",
        "unit": "comp",
        "quantity": "150.00",
        "min_stock": "30.00",
        "batch_number": "AMX-2401",
        "expiration_date": "2027-06-30",
        "supplier": "VetFarma Ltda",
        "unit_price": "2.50",
    },
    {
        "name": "Dipirona 50mg/ml",
        "generic_name": "Dipirona",
        "category": "analgesico",
        "unit": "ml",
        "quantity": "500.00",
        "min_stock": "80.00",
        "batch_number": "DIP-2402",
        "expiration_date": "2027-12-31",
        "supplier": "MedVet Distribuidora",
        "unit_price": "0.85",
    },
    {
        "name": "Vacina V10",
        "generic_name": "Polivalente canina",
        "category": "vacina",
        "unit": "dose",
        "quantity": "45.00",
        "min_stock": "15.00",
        "batch_number": "VAC-2026-A",
        "expiration_date": "2026-12-31",
        "supplier": "BioVet Imunobiológicos",
        "unit_price": "35.00",
    },
]

DEMO_USER_EMAILS = {item["email"] for item in DEMO_USERS}
DEMO_CLIENT_EMAILS = {item["email"] for item in DEMO_CLIENTS}
DEMO_ANIMAL_NAMES = {item["name"] for item in DEMO_ANIMALS}
DEMO_VET_CRMVS = {item["crmv"] for item in DEMO_VETERINARIANS}
DEMO_MEDICINE_NAMES = {item["name"] for item in DEMO_MEDICINES}
