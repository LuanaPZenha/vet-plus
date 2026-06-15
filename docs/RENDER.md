# Deploy no Render — Opção A (Auth Service)

Guia para publicar a **API de autenticação** do Vet Plus+ no Render.

> O sistema completo (6 APIs + frontend) roda localmente com `docker compose up`.

---

## Dockerfile na raiz

O repositório inclui `./Dockerfile` na raiz para deploy no Render (microsserviço **auth**).

| Campo no Render | Valor |
|-----------------|--------|
| Root Directory | *(vazio)* |
| Dockerfile Path | `Dockerfile` *(padrão)* |
| Runtime | Docker |

---

## Blueprint (recomendado)

1. **New +** → **Blueprint**
2. Repositório `LuanaPZenha/vet-plus`
3. **Apply** (usa `render.yaml`)

---

## Configuração manual

1. **New +** → **Web Service** → conecte o repo
2. **Runtime:** Docker
3. Crie **PostgreSQL** no Render
4. **Environment Variables:**

| Key | Value |
|-----|--------|
| `DATABASE_URL` | Internal Database URL do Postgres |
| `SECRET_KEY` | chave longa aleatória |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com,localhost,127.0.0.1` |

5. **Health Check Path:** `/api/docs/`
6. **Deploy**

---

## Testar

```
https://SEU-SERVICO.onrender.com/api/docs/
```

```bash
curl -X POST https://SEU-SERVICO.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@vet.com\",\"password\":\"senha1234\",\"full_name\":\"Admin\",\"role\":\"admin\"}"
```

---

## Erros comuns

| Erro | Solução |
|------|---------|
| `open Dockerfile: no such file or directory` | Confirme push com `Dockerfile` na raiz |
| `DisallowedHost` | `ALLOWED_HOSTS=.onrender.com,...` |
| App não responde | Render usa `$PORT` — já configurado no Dockerfile |
