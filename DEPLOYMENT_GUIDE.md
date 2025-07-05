# Руководство по развертыванию в production

## Обзор

Данное руководство описывает процесс развертывания HTMLpageGen в production окружении с высокой доступностью, безопасностью и производительностью.

## Архитектура production

### Компоненты системы

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │  Frontend   │    │   Backend   │
│ (Reverse    │────│  (Next.js)  │────│  (FastAPI)  │
│  Proxy)     │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                                      │
       └────────────────┐                     │
                        │                     │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Redis     │    │ PostgreSQL  │    │ Monitoring  │
│  (Cache)    │    │ (Database)  │    │(Prometheus) │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Требования к серверу

#### Минимальная конфигурация

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Диск**: 20 GB SSD
- **ОС**: Ubuntu 20.04+ / CentOS 8+ / RHEL 8+

#### Рекомендуемая конфигурация

- **CPU**: 4 cores
- **RAM**: 8 GB
- **Диск**: 50 GB SSD
- **ОС**: Ubuntu 22.04 LTS

#### High-load конфигурация

- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Диск**: 100+ GB NVMe SSD
- **Балансировщик нагрузки**: HAProxy/CloudFlare

## Методы развертывания

### Метод 1: Docker Compose (Рекомендуется)

#### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Клонирование и настройка

```bash
# Клонирование репозитория
git clone https://github.com/your-username/HTMLpageGen.git
cd HTMLpageGen

# Создание production конфигурации
cp .env.production.example .env.production
cp backend/.env.production.example backend/.env.production
cp frontend/.env.production.example frontend/.env.production
```

#### 3. Настройка переменных окружения

**backend/.env.production:**

```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=HTMLpageGen
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql://htmlpagegen:secure_password@postgres:5432/htmlpagegen_prod

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-super-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# CORS
BACKEND_CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
PROMETHEUS_ENABLED=true
LOG_LEVEL=WARNING

# SSL
SSL_VERIFY=true
```

**frontend/.env.production:**

```env
# API URLs
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_FRONTEND_URL=https://yourdomain.com

# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_api_key

# Analytics
NEXT_PUBLIC_GA_ID=GA_MEASUREMENT_ID
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn

# Performance
NEXT_PUBLIC_DEBUG=false
NEXT_PUBLIC_COMPRESSION=true
```

#### 4. SSL сертификаты

**Автоматические SSL (Let's Encrypt):**

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Ручные SSL сертификаты:**

```bash
# Создание директории для сертификатов
mkdir -p ssl
cp your-domain.crt ssl/fullchain.pem
cp your-domain.key ssl/privkey.pem
```

#### 5. Запуск production

```bash
# Сборка и запуск
docker-compose -f docker-compose.prod.yml up -d --build

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
```

### Метод 2: Kubernetes

#### 1. Подготовка манифестов

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: htmlpagegen

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: htmlpagegen-config
  namespace: htmlpagegen
data:
  DATABASE_URL: "postgresql://user:pass@postgres:5432/htmlpagegen"
  REDIS_URL: "redis://redis:6379/0"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: htmlpagegen-secrets
  namespace: htmlpagegen
type: Opaque
stringData:
  SECRET_KEY: "your-secret-key"
  DEEPSEEK_API_KEY: "your-deepseek-key"
  SENTRY_DSN: "your-sentry-dsn"
```

#### 2. Развертывание Backend

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: htmlpagegen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: htmlpagegen/backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                configMapKeyRef:
                  name: htmlpagegen-config
                  key: DATABASE_URL
            - name: SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: htmlpagegen-secrets
                  key: SECRET_KEY
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

#### 3. Развертывание Frontend

```yaml
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: htmlpagegen
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: htmlpagegen/frontend:latest
          ports:
            - containerPort: 3000
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "https://api.yourdomain.com"
```

#### 4. Ingress конфигурация

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: htmlpagegen-ingress
  namespace: htmlpagegen
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
    - hosts:
        - yourdomain.com
        - www.yourdomain.com
      secretName: htmlpagegen-tls
  rules:
    - host: yourdomain.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 3000
```

### Метод 3: Ручная установка

#### 1. Подготовка сервера

```bash
# Установка зависимостей
sudo apt update
sudo apt install -y python3.11 python3-pip nodejs npm nginx postgresql redis-server

# Создание пользователя
sudo useradd -m -s /bin/bash htmlpagegen
sudo usermod -aG sudo htmlpagegen
```

#### 2. Установка Backend

```bash
# Переключение на пользователя
sudo su - htmlpagegen

# Клонирование
git clone https://github.com/your-username/HTMLpageGen.git
cd HTMLpageGen/backend

# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка базы данных
sudo -u postgres createdb htmlpagegen_prod
sudo -u postgres createuser htmlpagegen_user

# Создание systemd сервиса
sudo tee /etc/systemd/system/htmlpagegen-backend.service > /dev/null <<EOF
[Unit]
Description=HTMLpageGen Backend
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=htmlpagegen
Group=htmlpagegen
WorkingDirectory=/home/htmlpagegen/HTMLpageGen/backend
Environment=PATH=/home/htmlpagegen/HTMLpageGen/backend/venv/bin
ExecStart=/home/htmlpagegen/HTMLpageGen/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Запуск сервиса
sudo systemctl enable htmlpagegen-backend
sudo systemctl start htmlpagegen-backend
```

#### 3. Установка Frontend

```bash
cd /home/htmlpagegen/HTMLpageGen/frontend

# Установка зависимостей
npm ci --production

# Сборка
npm run build

# PM2 для управления процессом
npm install -g pm2

# Создание конфигурации PM2
tee ecosystem.config.js > /dev/null <<EOF
module.exports = {
  apps: [{
    name: 'htmlpagegen-frontend',
    script: 'npm',
    args: 'start',
    cwd: '/home/htmlpagegen/HTMLpageGen/frontend',
    instances: 2,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
}
EOF

# Запуск через PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### 4. Настройка Nginx

```nginx
# /etc/nginx/sites-available/htmlpagegen
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # API Proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/htmlpagegen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Мониторинг и логирование

### Prometheus и Grafana

#### 1. Docker Compose конфигурация

```yaml
# monitoring/docker-compose.yml
version: "3.8"
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
```

#### 2. Prometheus конфигурация

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "htmlpagegen-backend"
    static_configs:
      - targets: ["backend:8000"]

  - job_name: "nginx"
    static_configs:
      - targets: ["nginx:9113"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

### Централизованное логирование (ELK Stack)

#### 1. Elasticsearch + Logstash + Kibana

```yaml
# logging/docker-compose.yml
version: "3.8"
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
```

## Резервное копирование

### Автоматическое резервное копирование

```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/$DATE"
mkdir -p $BACKUP_DIR

# Резервная копия базы данных
docker exec htmlpagegen_postgres_1 pg_dump -U htmlpagegen htmlpagegen_prod > $BACKUP_DIR/database.sql

# Резервная копия Redis
docker exec htmlpagegen_redis_1 redis-cli BGSAVE
docker cp htmlpagegen_redis_1:/data/dump.rdb $BACKUP_DIR/redis.rdb

# Резервная копия проектов
tar -czf $BACKUP_DIR/projects.tar.gz /var/lib/htmlpagegen/projects/

# Загрузка в облако (AWS S3)
aws s3 cp $BACKUP_DIR/ s3://your-backup-bucket/$DATE/ --recursive

# Очистка старых резервных копий (старше 30 дней)
find /backups -type d -mtime +30 -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR"
```

### Настройка cron

```bash
# Редактирование crontab
crontab -e

# Ежедневное резервное копирование в 2:00
0 2 * * * /home/htmlpagegen/HTMLpageGen/scripts/backup.sh
```

## Масштабирование

### Горизонтальное масштабирование

#### 1. Балансировщик нагрузки (HAProxy)

```
# /etc/haproxy/haproxy.cfg
global
    daemon

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend htmlpagegen_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/yourdomain.pem
    redirect scheme https if !{ ssl_fc }
    default_backend htmlpagegen_backend

backend htmlpagegen_backend
    balance roundrobin
    server web1 10.0.0.10:3000 check
    server web2 10.0.0.11:3000 check
    server web3 10.0.0.12:3000 check

backend htmlpagegen_api
    balance roundrobin
    server api1 10.0.0.20:8000 check
    server api2 10.0.0.21:8000 check
    server api3 10.0.0.22:8000 check
```

#### 2. Docker Swarm

```bash
# Инициализация Swarm
docker swarm init

# Масштабирование сервисов
docker service create --replicas 3 --name htmlpagegen-backend htmlpagegen/backend:latest
docker service create --replicas 2 --name htmlpagegen-frontend htmlpagegen/frontend:latest

# Обновление сервиса
docker service update --image htmlpagegen/backend:v2.0.0 htmlpagegen-backend
```

### Вертикальное масштабирование

#### 1. Увеличение ресурсов Docker

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G
        reservations:
          cpus: "1.0"
          memory: 2G

  frontend:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 2G
```

#### 2. Оптимизация базы данных

```sql
-- PostgreSQL оптимизация
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

SELECT pg_reload_conf();
```

## Безопасность

### Firewall настройки

```bash
# UFW конфигурация
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Fail2Ban

```ini
# /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 10
```

### Обновления безопасности

```bash
#!/bin/bash
# scripts/security-updates.sh

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Обновление Docker образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Проверка CVE
docker scout cves htmlpagegen/backend:latest
docker scout cves htmlpagegen/frontend:latest

echo "Security updates completed"
```

## Проверка и тестирование

### Health checks

```bash
#!/bin/bash
# scripts/health-check.sh

# Проверка frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: FAIL"
    exit 1
fi

# Проверка backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend: OK"
else
    echo "❌ Backend: FAIL"
    exit 1
fi

# Проверка базы данных
if docker exec htmlpagegen_postgres_1 pg_isready > /dev/null 2>&1; then
    echo "✅ Database: OK"
else
    echo "❌ Database: FAIL"
    exit 1
fi

echo "🎉 All services are healthy"
```

### Нагрузочное тестирование

```bash
# Установка Apache Bench
sudo apt install apache2-utils

# Тестирование frontend
ab -n 1000 -c 10 http://yourdomain.com/

# Тестирование API
ab -n 500 -c 5 -p data.json -T application/json http://yourdomain.com/api/generate
```

## Rollback стратегия

### Blue-Green развертывание

```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

CURRENT_ENV=${1:-blue}
NEW_ENV=${2:-green}

echo "Deploying to $NEW_ENV environment..."

# Сборка новой версии
docker-compose -f docker-compose.$NEW_ENV.yml up -d --build

# Проверка здоровья
sleep 30
if ! curl -f http://localhost:3001/health; then
    echo "Health check failed, rolling back..."
    docker-compose -f docker-compose.$NEW_ENV.yml down
    exit 1
fi

# Переключение трафика
sudo nginx -s reload

echo "Successfully deployed to $NEW_ENV"
```

---

_Это руководство обеспечивает надежное развертывание HTMLpageGen в production. Регулярно обновляйте систему и следите за безопасностью._
