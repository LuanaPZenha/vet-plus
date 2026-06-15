#!/usr/bin/env python3
"""Popula os microsserviços Vet+ com dados de demonstração."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_DIR = ROOT / "data" / "seed"

BASE_URLS = {
    "auth": "http://localhost:8001/api",
    "clients": "http://localhost:8002/api",
    "animals": "http://localhost:8003/api",
    "consultations": "http://localhost:8004/api",
    "vaccination": "http://localhost:8005/api",
    "inventory": "http://localhost:8006/api",
}

DEFAULT_LOGIN = {"email": "admin@vet.com", "password": "senha1234"}


def load_json(name: str) -> list[dict]:
    path = SEED_DIR / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def request(method: str, url: str, token: str | None = None, payload: dict | None = None) -> dict | list:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        raise RuntimeError(f"{method} {url} -> {exc.code}: {detail}") from exc


def login() -> tuple[str, int]:
    response = request("POST", f"{BASE_URLS['auth']}/login/", payload=DEFAULT_LOGIN)
    return response["access_token"], response["user_id"]


def ensure_veterinarian(token: str, user_id: int) -> int:
    veterinarians = request("GET", f"{BASE_URLS['consultations']}/veterinarios/", token=token)
    if veterinarians:
        return veterinarians[0]["id"]

    created = request(
        "POST",
        f"{BASE_URLS['consultations']}/veterinarios/",
        token=token,
        payload={
            "user_id": user_id,
            "full_name": "Dr. Admin Vet",
            "crmv": "SP-10001",
            "specialty": "Clínica Geral",
        },
    )
    return created["id"]


def seed_clients(token: str) -> list[int]:
    existing = request("GET", f"{BASE_URLS['clients']}/clientes/", token=token)
    if len(existing) >= 3:
        print(f"  clientes: {len(existing)} registros já existem, pulando")
        return [item["id"] for item in existing[:3]]

    client_ids: list[int] = []
    for item in load_json("clients.json"):
        created = request("POST", f"{BASE_URLS['clients']}/clientes/", token=token, payload=item)
        client_ids.append(created["id"])
        print(f"  + tutor: {created['nome_completo']} (id={created['id']})")
    return client_ids


def seed_animals(token: str, client_ids: list[int]) -> list[int]:
    existing = request("GET", f"{BASE_URLS['animals']}/animais/", token=token)
    if len(existing) >= 3:
        print(f"  animais: {len(existing)} registros já existem, pulando")
        return [item["id"] for item in existing[:3]]

    animal_ids: list[int] = []
    for item in load_json("animals.json"):
        payload = {key: value for key, value in item.items() if key != "client_index"}
        payload["client_id"] = client_ids[item["client_index"]]
        created = request("POST", f"{BASE_URLS['animals']}/animais/", token=token, payload=payload)
        animal_ids.append(created["id"])
        print(f"  + animal: {created['name']} (id={created['id']})")
    return animal_ids


def seed_consultations(token: str, animal_ids: list[int], veterinarian_id: int) -> None:
    existing = request("GET", f"{BASE_URLS['consultations']}/consultas/", token=token)
    if len(existing) >= 3:
        print(f"  consultas: {len(existing)} registros já existem, pulando")
        return

    for item in load_json("consultations.json"):
        payload = {
            "animal_id": animal_ids[item["animal_index"]],
            "veterinarian_id": veterinarian_id,
            "scheduled_at": item["scheduled_at"],
            "type": item["type"],
            "notes": item["notes"],
        }
        created = request("POST", f"{BASE_URLS['consultations']}/consultas/", token=token, payload=payload)
        print(f"  + consulta: animal #{created['animal_id']} — {created['type']} (id={created['id']})")


def seed_vaccines(token: str, animal_ids: list[int], veterinarian_id: int) -> None:
    existing = request("GET", f"{BASE_URLS['vaccination']}/vacinas/", token=token)
    if len(existing) >= 3:
        print(f"  vacinas: {len(existing)} registros já existem, pulando")
        return

    for item in load_json("vaccines.json"):
        payload = {
            "animal_id": animal_ids[item["animal_index"]],
            "vaccine_name": item["vaccine_name"],
            "application_date": item["application_date"],
            "next_dose_date": item.get("next_dose_date"),
            "veterinarian_id": veterinarian_id,
            "batch_number": item.get("batch_number"),
            "notes": item.get("notes"),
        }
        created = request("POST", f"{BASE_URLS['vaccination']}/vacinas/", token=token, payload=payload)
        print(f"  + vacina: {created['vaccine_name']} — {created['animal_id']} (id={created['id']})")


def seed_medicines(token: str) -> None:
    existing = request("GET", f"{BASE_URLS['inventory']}/medicamentos/", token=token)
    if len(existing) >= 3:
        print(f"  medicamentos: {len(existing)} registros já existem, pulando")
        return

    for item in load_json("medicines.json"):
        created = request("POST", f"{BASE_URLS['inventory']}/medicamentos/", token=token, payload=item)
        print(f"  + medicamento: {created['name']} (id={created['id']})")


def main() -> int:
    print("Vet+ — seed de dados de demonstração\n")

    token, user_id = login()
    print(f"Autenticado como user_id={user_id}\n")

    print("Tutores (clientes):")
    client_ids = seed_clients(token)

    print("\nAnimais:")
    animal_ids = seed_animals(token, client_ids)

    veterinarian_id = ensure_veterinarian(token, user_id)
    print(f"\nVeterinário id={veterinarian_id}")

    print("\nConsultas:")
    seed_consultations(token, animal_ids, veterinarian_id)

    print("\nVacinas:")
    seed_vaccines(token, animal_ids, veterinarian_id)

    print("\nEstoque (medicamentos):")
    seed_medicines(token)

    print("\nSeed concluído com sucesso.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"\nErro: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
