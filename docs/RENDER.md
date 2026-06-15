# Deploy no Render — Opção A (Auth Service)

Guia para publicar **apenas o microsserviço de autenticação** no Render, como demonstração acadêmica de deploy em cloud.

> O sistema completo (6 APIs + frontend) roda localmente com `docker compose up`. No Render free tier, subir tudo exigiria muitos serviços pagos/separados. Esta opção publica a API de login/registro com Swagger.

---

## Pré-requisitos

- Conta em [render.com](https://render.com)
- Repositório no GitHub: `LuanaPZenha/vet-plus`
- Código atualizado na branch `main`

---

## Método 1 — Blueprint (recomendado)

1. No Render, clique em **New +** → **Blueprint**
2. Conecte o repositório `vet-plus`
3. O Render detecta o arquivo `render.yaml` na raiz
4. Revise os recursos:
   - **vet-auth-db** — PostgreSQL (free)
   - **vet-plus-auth** — Web Service Docker (free)
5. Clique em **Apply**

O deploy leva alguns minutos. Ao concluir, a URL será algo como:

`https://vet-plus-auth.onrender.com`

---

## Método 2 — Configuração manual

Se preferir criar o serviço na mão:

### 1. Banco PostgreSQL

1. **New +** → **PostgreSQL**
2. Name: `vet-auth-db`
3. Plan: **Free**
4. Crie e copie a **Internal Database URL**

### 2. Web Service (Docker)

1. **New +** → **Web Service**
2. Conecte o repositório `vet-plus`
3. Configurações:

| Campo | Valor |
|-------|--------|
| Name | `vet-plus-auth` |
| Region | Oregon (ou mais próxima) |
| Branch | `main` |
| Root Directory | *(vazio — raiz do repo)* |
| Runtime | **Docker** |
| Dockerfile Path | `services/auth/Dockerfile` |
| Plan | Free |

4. **Environment Variables:**

| Key | Value |
|-----|--------|
| `DATABASE_URL` | Internal Database URL do Postgres |
| `SECRET_KEY` | Gere uma chave longa (64+ caracteres) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com,localhost,127.0.0.1` |

5. **Advanced** → Health Check Path: `/api/docs/`
6. **Create Web Service**

---

## Testar após o deploy

### Swagger (documentação interativa)

Abra no navegador:

```
https://SEU-SERVICO.onrender.com/api/docs/
```

### Registrar usuário

```bash
curl -X POST https://SEU-SERVICO.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@vet.com\",\"password\":\"senha1234\",\"full_name\":\"Admin Vet\",\"role\":\"admin\"}"
```

### Login

```bash
curl -X POST https://SEU-SERVICO.onrender.com/api/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@vet.com\",\"password\":\"senha1234\"}"
```

Resposta esperada: `access_token`, `user_id`, `role`.

---

## Erros comuns

| Erro | Causa | Solução |
|------|--------|---------|
| `open Dockerfile: no such file or directory` | Render procura Dockerfile na raiz | Use `services/auth/Dockerfile` |
| Build OK, app não responde | Porta errada | O Dockerfile usa `$PORT` do Render |
| `DisallowedHost` | Host não permitido | `ALLOWED_HOSTS=.onrender.com,...` |
| `connection refused` (DB) | URL externa vs interna | Use **Internal Database URL** |
| Serviço dorme (free tier) | Inatividade ~15 min | Primeira requisição demora ~30s |

---

## O que fica no ar vs local

| Recurso | Render (Opção A) | Local (`docker compose`) |
|---------|------------------|---------------------------|
| Auth API | ✅ | ✅ |
| Clients, Animals, etc. | ❌ | ✅ |
| Frontend dashboard | ❌ | ✅ http://localhost:3000 |
| Dados de demo (seed) | Manual via API | `python scripts/seed_data.py` |

Para apresentação acadêmica, você pode demonstrar:

1. **Deploy na cloud** — Swagger + login no Render
2. **Sistema completo** — rodando localmente com Docker

---

## Atualizar o deploy

Após push na branch `main`, o Render redeploya automaticamente (se Auto-Deploy estiver ativo):

```bash
git push origin main
```

Ou no dashboard: **Manual Deploy** → **Deploy latest commit**.
