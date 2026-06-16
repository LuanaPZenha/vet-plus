# Deploy no Render — stack completa Vet Plus+

## URL principal

**https://vet-plus.onrender.com** abre o **dashboard React** (login, clientes, animais, etc.).

As APIs ficam em serviços separados; o nginx do frontend faz proxy de `/api/*` para cada microsserviço (igual ao `docker compose` local).

| Serviço | URL |
|---------|-----|
| **App (frontend)** | https://vet-plus.onrender.com |
| Auth | https://vet-plus-auth.onrender.com |
| Clientes | https://vet-plus-clients.onrender.com |
| Animais | https://vet-plus-animals.onrender.com |
| Consultas | https://vet-plus-consultations.onrender.com |
| Vacinação | https://vet-plus-vaccination.onrender.com |
| Estoque | https://vet-plus-inventory.onrender.com |

---

## Migrar do deploy atual (só auth em vet-plus)

Se hoje `vet-plus` roda a API de auth:

1. Faça **push** deste código para `main`
2. No Render, crie um **novo Web Service** `vet-plus-auth`:
   - Dockerfile: `Dockerfile.auth`
   - Mesmo Postgres (`vet-auth-db`) → copie `DATABASE_URL` e `SECRET_KEY` do serviço antigo
3. Crie os outros 5 microsserviços + bancos (ou use **Blueprint** abaixo)
4. No serviço **vet-plus**, altere o Dockerfile para `./Dockerfile` (frontend) e adicione as env vars de proxy (`AUTH_URL`, `AUTH_HOST`, etc.) — o blueprint faz isso automaticamente
5. **Redeploy** todos os serviços

---

## Blueprint (recomendado)

1. Push para `main`
2. Render → **New +** → **Blueprint** → repo `LuanaPZenha/vet-plus` → **Apply**

---

## Testar

1. Abra https://vet-plus.onrender.com
2. Registre um usuário ou use credenciais criadas via `/api/register/` na auth
3. Navegue pelo dashboard

---

## Plano free

Cada serviço hiberna após ~15 min sem uso. A primeira requisição pode demorar ~50s. São 7 web services + 6 bancos.
