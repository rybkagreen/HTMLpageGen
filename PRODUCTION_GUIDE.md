# 🚀 Production Ready Deployment Guide

## 📋 Оглавление

1. [Архитектура системы](#архитектура-системы)
2. [Требования](#требования)
3. [Настройка окружения](#настройка-окружения)
4. [Деплой](#деплой)
5. [Мониторинг](#мониторинг)
6. [Безопасность](#безопасность)
7. [Резервное копирование](#резервное-копирование)
8. [Масштабирование](#масштабирование)
9. [Обслуживание](#обслуживание)

## 🏗️ Архитектура системы

### Компоненты

- **Frontend**: Next.js приложение с SSR/SSG
- **Backend**: FastAPI с async/await
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Reverse Proxy**: Nginx
- **Monitoring**: Prometheus + Grafana
- **Container Platform**: Docker + Docker Compose

### Безопасность

- HTTPS с TLS 1.2/1.3
- Security headers (CSP, HSTS, XSS Protection)
- Rate limiting
- Input validation
- Non-root containers
- Secret management

### Мониторинг

- Application metrics
- System metrics
- Health checks
- Structured logging (JSON)
- Error tracking (Sentry)
- Performance monitoring

## 📋 Требования

### Системные требования

- **OS**: Ubuntu 20.04+ / CentOS 8+ / RHEL 8+
- **CPU**: 4+ cores (рекомендуется 8+)
- **RAM**: 8GB+ (рекомендуется 16GB+)
- **Storage**: 100GB+ SSD
- **Network**: Стабильное интернет-соединение

### Программное обеспечение

- Docker 24.0+
- Docker Compose 2.0+
- Git 2.30+
- Certbot (для SSL)

### Домен и SSL

- Зарегистрированный домен
- DNS настройки
- SSL сертификат (Let's Encrypt или коммерческий)

## ⚙️ Настройка окружения

### 1. Подготовка сервера

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

# Перезапуск для применения изменений
sudo systemctl restart docker
newgrp docker
```

### 2. Клонирование проекта

```bash
cd /opt
sudo git clone https://github.com/yourorg/HTMLpageGen.git
sudo chown -R $USER:$USER HTMLpageGen
cd HTMLpageGen
```

### 3. Настройка environment файлов

```bash
# Скопировать и настроить production конфигурацию
cp backend/.env.production.example backend/.env.production

# Отредактировать конфигурацию
nano backend/.env.production
```

### 4. Настройка SSL

```bash
# Установка Certbot
sudo apt install certbot

# Получение SSL сертификата
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Копирование сертификатов
sudo mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown -R $USER:$USER nginx/ssl
```

### 5. Настройка firewall

```bash
# Установка UFW
sudo ufw enable

# Разрешение портов
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3001/tcp  # Grafana (опционально)
```

## 🚀 Деплой

### Автоматический деплой

```bash
# Проверка требований
./scripts/deploy.sh check

# Полный деплой
./scripts/deploy.sh deploy

# Проверка статуса
./scripts/deploy.sh status
```

### Ручной деплой

```bash
# 1. Сборка образов
docker-compose -f docker-compose.prod.yml build

# 2. Запуск сервисов
docker-compose -f docker-compose.prod.yml up -d

# 3. Проверка здоровья
curl -f https://yourdomain.com/health
```

### Проверка деплоя

```bash
# Проверка всех сервисов
docker-compose -f docker-compose.prod.yml ps

# Проверка логов
docker-compose -f docker-compose.prod.yml logs -f app

# Проверка ресурсов
docker stats
```

## 📊 Мониторинг

### Доступные дашборды

| Сервис          | URL                                    | Описание              |
| --------------- | -------------------------------------- | --------------------- |
| API Health      | https://yourdomain.com/health          | Статус API            |
| Detailed Health | https://yourdomain.com/health/detailed | Детальная диагностика |
| Metrics         | https://yourdomain.com/metrics         | Метрики приложения    |
| Prometheus      | http://yourdomain.com:9090             | Метрики и алерты      |
| Grafana         | http://yourdomain.com:3001             | Дашборды мониторинга  |

### Ключевые метрики

- **Response Time**: < 200ms (95th percentile)
- **Error Rate**: < 1%
- **Uptime**: > 99.9%
- **CPU Usage**: < 70%
- **Memory Usage**: < 80%
- **Disk Usage**: < 85%

### Настройка алертов

```bash
# Настройка Slack уведомлений
export SLACK_WEBHOOK="your-slack-webhook-url"

# Настройка email уведомлений
# Отредактировать monitoring/alertmanager.yml
```

## 🔒 Безопасность

### Обязательные меры

1. **Изменить пароли по умолчанию**

   ```bash
   # Обновить в .env.production:
   - DB_PASSWORD
   - REDIS_PASSWORD
   - SECRET_KEY
   - GRAFANA_PASSWORD
   ```

2. **Настроить firewall**

   ```bash
   sudo ufw enable
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

3. **Отключить root login**

   ```bash
   sudo nano /etc/ssh/sshd_config
   # PermitRootLogin no
   sudo systemctl restart ssh
   ```

4. **Обновления безопасности**
   ```bash
   # Настроить автоматические обновления
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure unattended-upgrades
   ```

### Регулярные проверки

```bash
# Аудит Docker образов
docker scan htmlpagegen-app:latest

# Проверка SSL сертификата
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Анализ логов безопасности
sudo grep "Failed password" /var/log/auth.log
```

## 💾 Резервное копирование

### Автоматическое резервное копирование

```bash
# Создание cron задачи
crontab -e

# Добавить строку для ежедневного бэкапа в 2:00
0 2 * * * /opt/HTMLpageGen/scripts/backup.sh
```

### Ручное резервное копирование

```bash
# Создание бэкапа БД
./scripts/deploy.sh backup

# Резервное копирование файлов
tar -czf backup_$(date +%Y%m%d).tar.gz \
  --exclude='node_modules' \
  --exclude='.git' \
  /opt/HTMLpageGen
```

### Восстановление

```bash
# Восстановление БД
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U htmlpagegen -d htmlpagegen_prod < backup.sql

# Перезапуск сервисов
docker-compose -f docker-compose.prod.yml restart
```

## ⚡ Масштабирование

### Горизонтальное масштабирование

```bash
# Увеличение количества воркеров
docker-compose -f docker-compose.prod.yml up -d --scale app=3

# Настройка load balancer в nginx.conf
upstream backend {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}
```

### Вертикальное масштабирование

```bash
# Обновление лимитов ресурсов в docker-compose.prod.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Кэширование

```bash
# Настройка Redis Cluster для высокой доступности
# Добавление CDN для статических файлов
# Настройка database connection pooling
```

## 🛠️ Обслуживание

### Регулярные задачи

#### Еженедельно

- Проверка логов ошибок
- Анализ метрик производительности
- Обновление зависимостей (dev среда)

#### Ежемесячно

- Обновление системы
- Ротация логов
- Анализ использования ресурсов
- Тестирование процедуры восстановления

#### Ежеквартально

- Аудит безопасности
- Планирование масштабирования
- Обновление документации

### Команды обслуживания

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# Очистка ресурсов Docker
docker system prune -a

# Обновление образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Проверка производительности
htop
df -h
free -h
```

### Устранение неполадок

#### Проблема: Высокая нагрузка на CPU

```bash
# Анализ процессов
docker stats
htop

# Масштабирование
docker-compose -f docker-compose.prod.yml up -d --scale app=2
```

#### Проблема: Медленные запросы к БД

```bash
# Анализ запросов PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U htmlpagegen -c "SELECT * FROM pg_stat_activity;"

# Оптимизация индексов
```

#### Проблема: Переполнение диска

```bash
# Очистка логов Docker
docker system prune -a --volumes

# Ротация логов приложения
find /var/log -name "*.log" -mtime +30 -delete
```

## 📞 Поддержка

### Контакты

- **Email**: support@yourdomain.com
- **Slack**: #htmlpagegen-support
- **Documentation**: https://docs.yourdomain.com

### Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Версия**: 1.0.0  
**Дата обновления**: 4 июля 2025  
**Статус**: ✅ Production Ready
