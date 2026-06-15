# Deploy no Render — Opção A (Auth Service)

Guia para publicar **apenas o microsserviço de autenticação** no Render.

---

## Erro: `open Dockerfile: no such file or directory`

O Render procura `./Dockerfile` na raiz por padrão. Neste projeto o arquivo correto é:

```
services/auth/Dockerfile
```

Configure esse caminho em **Settings → Build & Deploy → Dockerfile Path**.

---

## Configuração manual (serviço existente)

1. **Settings → Build & Deploy**

| Campo | Valor |
|-------|--------|
| Root Directory | *(vazio)* |
| Dockerfile Path | `services/auth/Dockerfile` |
| Branch | `main` |

2. **Settings → Environment**

| Key | Value |
|-----|--------|
| `DATABASE_URL` | Internal Database URL do Postgres Render |
| `SECRET_KEY` | chave longa aleatória |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com,localhost,127.0.0.1` |

3. Crie um **PostgreSQL** no Render (se ainda não tiver) e vincule a URL interna.

4. **Manual Deploy → Deploy latest commit**

---

## Blueprint (novo deploy)

1. **New + → Blueprint**
2. Repositório `LuanaPZenha/vet-plus`
3. **Apply** (usa `render.yaml` da raiz)

---

## Testar

- Swagger: `https://SEU-SERVICO.onrender.com/api/docs/`

```bash
curl -X POST https://SEU-SERVICO.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@vet.com\",\"password\":\"senha1234\",\"full_name\":\"Admin\",\"role\":\"admin\"}"
```
