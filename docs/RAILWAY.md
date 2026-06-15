# Deploy no Railway — microsserviço Auth (Opção A)

Publica a **API de autenticação** do Vet+ no Railway usando `start.sh` na raiz.

> O sistema completo (6 APIs + frontend) continua rodando localmente com `docker compose up`.

---

## Arquivos de deploy

| Arquivo | Função |
|---------|--------|
| `start.sh` | Migra o banco e inicia Gunicorn |
| `requirements.txt` | Dependências Python (build Railway) |
| `railway.toml` | Comando de start no deploy |

---

## Passo a passo no Railway

### 1. Novo projeto
1. Acesse [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. Selecione `LuanaPZenha/vet-plus`
4. Branch: `main`

### 2. PostgreSQL
1. No projeto, clique **+ New** → **Database** → **PostgreSQL**
2. Abra o Postgres → **Variables** → copie `DATABASE_URL`

### 3. Variáveis do Web Service
No serviço da aplicação (não no banco), em **Variables**:

| Variável | Valor |
|----------|--------|
| `DATABASE_URL` | Referência ao Postgres (`${{Postgres.DATABASE_URL}}`) |
| `SECRET_KEY` | Chave longa aleatória (64+ caracteres) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.railway.app,localhost,127.0.0.1` |

> Railway injeta `PORT` automaticamente — o `start.sh` já usa essa variável.

### 4. Configurações de build (se necessário)
Em **Settings** do serviço:
- **Root Directory:** *(vazio — raiz do repo)*
- **Start Command:** `bash start.sh` *(já definido no `railway.toml`)*

### 5. Deploy
Railway faz build e deploy automaticamente após o push no GitHub.

---

## Testar

Substitua pela URL gerada pelo Railway (ex.: `https://vet-plus-production.up.railway.app`):

```
https://SUA-URL.railway.app/api/docs/
```

Registrar admin:

```bash
curl -X POST https://SUA-URL.railway.app/api/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@vet.com\",\"password\":\"senha1234\",\"full_name\":\"Admin Vet\",\"role\":\"admin\"}"
```

---

## Erros comuns

| Erro | Solução |
|------|---------|
| `start.sh: not found` | Confirme que o arquivo está na raiz e commitado |
| `Permission denied` | Start command: `bash start.sh` (não `./start.sh`) |
| `DisallowedHost` | `ALLOWED_HOSTS=.railway.app,...` |
| Build sem Python | `requirements.txt` deve estar na raiz |
| Banco não conecta | Vincule `DATABASE_URL` ao Postgres do Railway |

---

## Alternativa: Docker

Se preferir Docker em vez de Nixpacks + `start.sh`:

1. **Settings** → Builder: **Dockerfile**
2. **Dockerfile path:** `services/auth/Dockerfile`
3. Remova ou ignore o `start.sh` (o Dockerfile já inicia o serviço)
