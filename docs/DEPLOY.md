# Guia de Deploy — Vet Plus+ em Ubuntu Server

Este guia descreve o processo completo de deploy do sistema Vet Plus+ em um servidor Linux Ubuntu.

---

## Pré-requisitos

- Servidor Ubuntu 22.04 LTS ou 24.04 LTS
- Acesso SSH com privilégios sudo
- Portas abertas: 8001–8005 (APIs), 22 (SSH)
- Mínimo: 2 GB RAM, 20 GB disco

---

## 1. Preparação do Servidor

### 1.1 Atualizar o sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Criar usuário de deploy (recomendado)

```bash
sudo adduser vetdeploy
sudo usermod -aG sudo vetdeploy
su - vetdeploy
```

### 1.3 Configurar firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 8001:8005/tcp
sudo ufw enable
sudo ufw status
```

---

## 2. Instalar Docker

### 2.1 Dependências

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

### 2.2 Chave GPG e repositório oficial

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.3 Instalar Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 2.4 Adicionar usuário ao grupo docker

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 2.5 Verificar instalação

```bash
docker --version
docker compose version
docker run hello-world
```

---

## 3. Instalar Docker Compose (standalone, se necessário)

O plugin `docker compose` já vem com Docker CE moderno. Se precisar da versão standalone:

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

---

## 4. Deploy da Aplicação

### 4.1 Clonar o repositório

```bash
cd /opt
sudo git clone https://github.com/seu-usuario/vet-plus.git
sudo chown -R $USER:$USER vet-plus
cd vet-plus
```

### 4.2 Configurar variáveis de ambiente

```bash
cp .env.example .env
nano .env
```

**Conteúdo recomendado para produção:**

```env
DB_PASSWORD=senha_forte_aleatoria_aqui
SECRET_KEY=chave_secreta_aleatoria_64_caracteres_minimo
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,IP_DO_SERVIDOR,localhost
```

> Gere uma SECRET_KEY segura:
> ```bash
> python3 -c "import secrets; print(secrets.token_urlsafe(64))"
> ```

### 4.3 Build e subida dos containers

```bash
docker compose up --build -d
```

### 4.4 Verificar status

```bash
docker compose ps
docker compose logs -f --tail=50
```

Todos os 10 containers (5 serviços + 5 bancos) devem estar `running`/`healthy`.

### 4.5 Testar endpoints

```bash
# Health check básico
curl -s http://localhost:8001/api/docs/ | head -5
curl -s http://localhost:8002/api/docs/ | head -5

# Registrar admin
curl -X POST http://localhost:8001/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vet.com","password":"Admin@2024!","full_name":"Admin","role":"admin"}'
```

---

## 5. Configuração com Nginx (Reverso Proxy)

Para produção, use Nginx como proxy reverso com HTTPS.

### 5.1 Instalar Nginx e Certbot

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### 5.2 Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/vet-plus
```

```nginx
upstream auth_service {
    server 127.0.0.1:8001;
}
upstream clients_service {
    server 127.0.0.1:8002;
}
upstream animals_service {
    server 127.0.0.1:8003;
}
upstream consultations_service {
    server 127.0.0.1:8004;
}
upstream vaccination_service {
    server 127.0.0.1:8005;
}

server {
    listen 80;
    server_name api.vetclinic.com;

    location /auth/ {
        proxy_pass http://auth_service/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /clientes/ {
        proxy_pass http://clients_service/api/clientes/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /animais/ {
        proxy_pass http://animals_service/api/animais/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /consultas/ {
        proxy_pass http://consultations_service/api/consultas/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /vacinas/ {
        proxy_pass http://vaccination_service/api/vacinas/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/vet-plus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5.3 HTTPS com Let's Encrypt

```bash
sudo certbot --nginx -d api.vetclinic.com
```

---

## 6. Atualizações Futuras

### 6.1 Atualizar código

```bash
cd /opt/vet-plus
git pull origin main
docker compose up --build -d
```

### 6.2 Atualizar um serviço específico

```bash
docker compose up --build -d consultations-service
```

### 6.3 Ver logs de um serviço

```bash
docker compose logs -f auth-service
docker compose logs -f consultations-service --tail=100
```

### 6.4 Executar migrações manualmente

```bash
docker compose exec auth-service python manage.py migrate
docker compose exec consultations-service python manage.py migrate
```

### 6.5 Backup dos bancos de dados

```bash
# Script de backup
mkdir -p /opt/backups
for db in auth_db clients_db animals_db consultations_db vaccination_db; do
  docker compose exec -T ${db%-db}-db pg_dump -U vet_user $db > /opt/backups/${db}_$(date +%Y%m%d).sql
done
```

### 6.6 Restaurar backup

```bash
cat /opt/backups/auth_db_20240614.sql | \
  docker compose exec -T auth-db psql -U vet_user auth_db
```

---

## 7. Monitoramento

### 7.1 Verificar saúde dos containers

```bash
docker compose ps
docker stats --no-stream
```

### 7.2 Reiniciar serviços

```bash
docker compose restart
# ou serviço específico:
docker compose restart auth-service
```

### 7.3 Parar tudo

```bash
docker compose down
# Com remoção de volumes (CUIDADO - apaga dados):
# docker compose down -v
```

---

## 8. Systemd (Inicialização Automática)

Docker já reinicia containers com `restart: unless-stopped`. Para garantir que o Docker inicie no boot:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Opcional — serviço systemd para o compose:

```bash
sudo nano /etc/systemd/system/vet-plus.service
```

```ini
[Unit]
Description=Vet Plus+ Microservices
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/vet-plus
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable vet-plus
sudo systemctl start vet-plus
```

---

## 9. Checklist de Deploy

- [ ] Ubuntu atualizado
- [ ] Docker e Docker Compose instalados
- [ ] Repositório clonado em `/opt/vet-plus`
- [ ] `.env` configurado com senhas fortes
- [ ] `docker compose up --build -d` executado
- [ ] Todos os 10 containers running/healthy
- [ ] Teste de registro e login funcionando
- [ ] Nginx configurado (produção)
- [ ] HTTPS com Certbot (produção)
- [ ] Backup automatizado configurado
- [ ] Firewall configurado

---

## 10. Troubleshooting

| Problema | Solução |
|----------|---------|
| Container reinicia em loop | `docker compose logs <serviço>` — verificar DATABASE_URL |
| JWT inválido entre serviços | Verificar se `SECRET_KEY` é igual em todos os serviços |
| Banco não conecta | Aguardar health check: `docker compose ps` |
| Porta em uso | `sudo lsof -i :8001` e matar processo conflitante |
| Permissão Docker | `sudo usermod -aG docker $USER && newgrp docker` |
