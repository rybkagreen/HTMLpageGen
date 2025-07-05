# 🚀 Production Deployment - HTML Page Generator

Этот документ содержит краткое руководство по production-деплою HTML Page Generator. Для полного руководства см. [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md).

## 📦 Быстрый старт

### 1. Подготовка сервера

```bash
# Установка Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo pip3 install docker-compose

# Клонирование проекта
git clone <your-repo-url>
cd HTMLpageGen
```

### 2. Настройка окружения

```bash
# Копирование конфигурации
cp backend/.env.production.example backend/.env.production

# Редактирование конфигурации
nano backend/.env.production
```

⚠️ **Обязательно настройте:**

- `SECRET_KEY` (сгенерируйте безопасный ключ)
- `DATABASE_URL` (настройки PostgreSQL)
- `ALLOWED_HOSTS` (ваш домен)
- `AI_PROVIDER` и соответствующие API ключи
- `SENTRY_DSN` (для мониторинга ошибок)

### 3. Запуск в production

```bash
# Быстрый запуск
./scripts/start-production.sh

# Или через Docker Compose
docker-compose -f docker-compose.prod.yml up -d --build
```

### 4. Проверка работоспособности

```bash
# Health check
./scripts/health-check.sh

# Проверка логов
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Управление

### Основные команды

```bash
# Запуск
./scripts/start-production.sh

# Остановка
./scripts/stop-production.sh

# Health check
./scripts/health-check.sh

# Backup
./scripts/backup.sh

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
```

### Мониторинг

- **Health Check**: `http://your-domain/health`
- **Detailed Health**: `http://your-domain/health/detailed`
- **Metrics**: `http://your-domain/metrics`
- **Grafana**: `http://your-domain:3001` (admin/admin)
- **Prometheus**: `http://your-domain:9090`

### Endpoints

- **Frontend**: `http://your-domain`
- **Backend API**: `http://your-domain/api/v1`
- **API Docs**: `http://your-domain/docs` (если включено)

## 🛡️ Безопасность

### SSL/TLS сертификаты

```bash
# Получение Let's Encrypt сертификатов
certbot --nginx -d your-domain.com -d www.your-domain.com

# Автопродление
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

### Firewall

```bash
# Настройка UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📊 Мониторинг и алерты

### Cron jobs

```bash
# Добавление в crontab
crontab -e

# Health check каждые 5 минут
*/5 * * * * /opt/htmlpagegen/scripts/health-check.sh quiet

# Backup каждый день в 3:00
0 3 * * * /opt/htmlpagegen/scripts/backup.sh
```

### Системный сервис

```bash
# Установка systemd service
sudo cp deployment/htmlpagegen.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable htmlpagegen
sudo systemctl start htmlpagegen
```

## 🔄 Обновление

```bash
# Получение обновлений
git pull origin main

# Пересборка и перезапуск
docker-compose -f docker-compose.prod.yml up -d --build

# Или используйте скрипт деплоя
./scripts/deploy.sh
```

## 📋 Checklist для production

- [ ] Настроен безопасный `SECRET_KEY`
- [ ] Настроена база данных PostgreSQL
- [ ] Настроены CORS (`ALLOWED_HOSTS`)
- [ ] Настроены SSL сертификаты
- [ ] Настроен мониторинг (Sentry)
- [ ] Настроены backup'ы
- [ ] Настроен firewall
- [ ] Настроены алерты
- [ ] Отключен debug режим
- [ ] Проведено нагрузочное тестирование

## 🆘 Troubleshooting

### Проблемы с запуском

```bash
# Проверка статуса контейнеров
docker-compose -f docker-compose.prod.yml ps

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend

# Проверка health endpoints
curl http://localhost:8000/health
```

### Проблемы с производительностью

```bash
# Проверка ресурсов
docker stats

# Проверка метрик
curl http://localhost:8000/metrics

# Мониторинг системы
htop
```

### Восстановление из backup

```bash
# Список доступных backup'ов
./scripts/backup.sh list

# Восстановление
./scripts/backup.sh restore backup_name.tar.gz
```

## 📞 Поддержка

- **Документация**: [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
- **Health Check**: `./scripts/health-check.sh`
- **Логи**: `docker-compose -f docker-compose.prod.yml logs`
- **Мониторинг**: Grafana Dashboard

---

**⚡ Production Ready!** Этот проект готов к production-деплою со всеми необходимыми компонентами для надежной работы.
