# Deploy no Render — stack completa Vet Plus+

## URL principal

**https://vet-plus.onrender.com** abre o **dashboard React** (login, clientes, animais, etc.).

No Render, o serviço **vet-plus** (frontend) embute os microsserviços de clientes, animais, consultas, vacinação e estoque. O nginx faz proxy de `/api/*` para essas APIs locais e para o auth externo — igual ao `docker compose` local.

| Serviço | URL |
|---------|-----|
| **App (frontend + APIs)** | https://vet-plus.onrender.com |
| Auth | https://vet-plus-auth.onrender.com |

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
2. Render → Blueprint **vet-plus** → **Manual sync**
3. Confirme que o sync aponta para o commit mais recente (ex.: `fa18a18` ou posterior)
4. Aguarde redeploy de **vet-plus** e **vet-plus-auth**

Serviços necessários: apenas **vet-plus** (frontend + APIs) e **vet-plus-auth** (login). Os microsserviços separados (`vet-plus-clients`, etc.) **não são mais usados** — pode removê-los manualmente no Render se existirem.

---

## Testar

1. Abra https://vet-plus.onrender.com
2. No console do navegador (`F12`), confira `window.__VET_PLUS_ENV__.BUILD_SHA` — deve ser `7071eb8` ou commit mais recente (não `17dbc1d`)
3. Entre com o usuário demo (criado automaticamente no deploy do auth):
   - **E-mail:** `admin@vet.com`
   - **Senha:** `senha1234`

Para desativar a criação automática do demo, defina `SKIP_DEMO_USER=true` no serviço `vet-plus-auth`.

### Dados demo automáticos (3 de cada)

No deploy, o sistema cria automaticamente **3 registros de exemplo** em cada microsserviço:

| Serviço | Exemplos |
|---------|----------|
| **Auth** | `admin@vet.com`, `dr.silva@vet.com`, `dr.costa@vet.com` (senha: `senha1234`) |
| **Clientes** | Maria Souza, Carlos Lima, Ana Costa |
| **Animais** | Rex, Mimi, Thor (vinculados aos tutores) |
| **Consultas** | 3 veterinários + 3 consultas agendadas |
| **Vacinas** | V10, Antirrábica, Giardia (vinculadas aos animais) |
| **Estoque** | Amoxicilina, Dipirona, Vacina V10 |

Para desativar o seed dos microsserviços embutidos, defina `SKIP_DEMO_DATA=true` no serviço `vet-plus`.

**Importante:** o serviço `vet-plus` precisa da mesma `SECRET_KEY` do auth (grupo `vet-shared` no blueprint) para validar tokens JWT.

### Redeploy manual (se o Render ficou no commit antigo)

1. Render → serviço **vet-plus** → **Manual Deploy** → **Clear build cache & deploy**
2. Repita em **vet-plus-auth**
3. Em **vet-plus** → **Environment**, confira se `SECRET_KEY` existe e é **igual** à de **vet-plus-auth**

---

## Plano free

O frontend hiberna após ~15 min sem uso. A primeira requisição pode demorar ~50s. São 2 web services (frontend + auth) + **1 banco Postgres** (`vet-auth-db`):

| Schema / uso | Dados |
|--------------|-------|
| `public` (auth) | Usuários e login |
| `clients`, `animals`, `vaccination`, etc. | Tutores, animais, consultas, vacinas e estoque |

Auth e APIs embutidas compartilham o **mesmo** `vet-auth-db` (limite do plano free: 1 banco). Cada microsserviço usa um schema PostgreSQL próprio, então os dados persistem entre redeploys e os serviços se comunicam via HTTP (ex.: vacina valida se o animal existe antes de salvar).
