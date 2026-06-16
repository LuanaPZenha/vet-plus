"""Cria schema PostgreSQL isolado antes das migrations Django (Render)."""

from __future__ import annotations

import os
import sys


def main() -> int:
    if len(sys.argv) < 2:
        return 0

    schema = sys.argv[1].strip()
    database_url = os.environ.get("DATABASE_URL", "")
    if not schema or not database_url.startswith("postgres"):
        return 0

    import psycopg2

    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
    finally:
        conn.close()

    print(f"Schema PostgreSQL pronto: {schema}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
