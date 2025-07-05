# Руководство по обслуживанию HTMLpageGen

## Ежедневные операции

### Проверка состояния системы

#### Быстрая проверка

```bash
# Запуск комплексной проверки
./scripts/health-check.sh

# Проверка логов за последний час
docker-compose logs --since 1h

# Проверка использования ресурсов
docker stats --no-stream
```

#### Детальная диагностика

```bash
# Проверка дискового пространства
df -h

# Проверка использования памяти
free -h

# Проверка загрузки CPU
top -bn1 | grep "Cpu(s)"

# Проверка сетевых соединений
netstat -tulpn | grep -E "(3000|8000|5432|6379)"
```

### Мониторинг метрик

#### Ключевые метрики для отслеживания

```bash
# Количество активных пользователей
curl -s http://localhost:8000/metrics | grep "active_users"

# Время отклика API
curl -s http://localhost:8000/metrics | grep "response_time"

# Количество ошибок
curl -s http://localhost:8000/metrics | grep "error_rate"

# Использование DeepSeek API
curl -s http://localhost:8000/metrics | grep "deepseek_requests"
```

## Еженедельные операции

### Обслуживание базы данных

#### PostgreSQL оптимизация

```bash
# Подключение к базе данных
docker exec -it htmlpagegen_postgres_1 psql -U htmlpagegen -d htmlpagegen_prod

# Анализ размера таблиц
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# VACUUM и ANALYZE
VACUUM ANALYZE;

# Обновление статистики
ANALYZE;

# Проверка индексов
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

#### Очистка старых данных

```sql
-- Удаление старых логов (старше 30 дней)
DELETE FROM application_logs
WHERE created_at < NOW() - INTERVAL '30 days';

-- Удаление неактивных сессий (старше 7 дней)
DELETE FROM user_sessions
WHERE last_activity < NOW() - INTERVAL '7 days';

-- Архивирование старых проектов (старше 90 дней)
INSERT INTO archived_projects
SELECT * FROM projects
WHERE updated_at < NOW() - INTERVAL '90 days'
AND is_active = false;

DELETE FROM projects
WHERE updated_at < NOW() - INTERVAL '90 days'
AND is_active = false;
```

### Обслуживание Redis

```bash
# Подключение к Redis
docker exec -it htmlpagegen_redis_1 redis-cli

# Проверка использования памяти
INFO memory

# Очистка устаревших ключей
EVAL "return #redis.call('keys', ARGV[1])" 0 "session:*"

# Принудительное сохранение
BGSAVE

# Проверка статистики
INFO stats
```

### Обновление зависимостей

#### Backend (Python)

```bash
cd backend

# Активация виртуального окружения
source venv/bin/activate

# Проверка устаревших пакетов
pip list --outdated

# Обновление в тестовой среде
pip install --upgrade pip
pip-review --auto

# Тестирование
python -m pytest tests/

# Обновление requirements.txt
pip freeze > requirements.txt
```

#### Frontend (Node.js)

```bash
cd frontend

# Проверка устаревших пакетов
npm outdated

# Обновление зависимостей
npm update

# Проверка уязвимостей
npm audit

# Исправление уязвимостей
npm audit fix

# Тестирование
npm test
npm run build
```

## Ежемесячные операции

### Резервное копирование

#### Полное резервное копирование

```bash
#!/bin/bash
# scripts/monthly-backup.sh

DATE=$(date +%Y%m%d)
BACKUP_ROOT="/backups/monthly/$DATE"
mkdir -p $BACKUP_ROOT

echo "Starting monthly backup..."

# 1. База данных
echo "Backing up database..."
docker exec htmlpagegen_postgres_1 pg_dump -U htmlpagegen htmlpagegen_prod | gzip > $BACKUP_ROOT/database.sql.gz

# 2. Redis данные
echo "Backing up Redis..."
docker exec htmlpagegen_redis_1 redis-cli BGSAVE
sleep 10
docker cp htmlpagegen_redis_1:/data/dump.rdb $BACKUP_ROOT/redis.rdb

# 3. Файлы проектов
echo "Backing up project files..."
tar -czf $BACKUP_ROOT/projects.tar.gz /var/lib/htmlpagegen/projects/

# 4. Конфигурационные файлы
echo "Backing up configurations..."
tar -czf $BACKUP_ROOT/configs.tar.gz \
    .env.production \
    docker-compose.prod.yml \
    nginx/nginx.conf \
    ssl/

# 5. Логи
echo "Backing up logs..."
tar -czf $BACKUP_ROOT/logs.tar.gz /var/log/htmlpagegen/

# 6. Метаданные
echo "Creating backup metadata..."
cat > $BACKUP_ROOT/metadata.json << EOF
{
    "backup_date": "$(date -Iseconds)",
    "version": "$(git rev-parse HEAD)",
    "services": {
        "frontend": "$(docker images htmlpagegen/frontend --format '{{.Tag}}' | head -1)",
        "backend": "$(docker images htmlpagegen/backend --format '{{.Tag}}' | head -1)"
    },
    "database_size": "$(du -sh $BACKUP_ROOT/database.sql.gz | cut -f1)",
    "total_size": "$(du -sh $BACKUP_ROOT | cut -f1)"
}
EOF

# 7. Загрузка в облако
if [ "$CLOUD_BACKUP" = "true" ]; then
    echo "Uploading to cloud storage..."
    aws s3 cp $BACKUP_ROOT/ s3://htmlpagegen-backups/monthly/$DATE/ --recursive
fi

# 8. Проверка целостности
echo "Verifying backup integrity..."
if [ -f "$BACKUP_ROOT/database.sql.gz" ] && [ -f "$BACKUP_ROOT/projects.tar.gz" ]; then
    echo "✅ Backup completed successfully"
    echo "📊 Backup size: $(du -sh $BACKUP_ROOT | cut -f1)"
else
    echo "❌ Backup failed - missing files"
    exit 1
fi

# 9. Очистка старых резервных копий (старше 6 месяцев)
find /backups/monthly -type d -mtime +180 -exec rm -rf {} +

echo "Monthly backup completed: $BACKUP_ROOT"
```

### Тестирование восстановления

```bash
#!/bin/bash
# scripts/test-restore.sh

BACKUP_DATE=${1:-$(date +%Y%m%d)}
BACKUP_PATH="/backups/monthly/$BACKUP_DATE"
TEST_PREFIX="test_restore_"

echo "Testing restore from backup: $BACKUP_DATE"

# 1. Создание тестовой базы данных
docker exec htmlpagegen_postgres_1 createdb ${TEST_PREFIX}htmlpagegen

# 2. Восстановление данных
gunzip -c $BACKUP_PATH/database.sql.gz | \
docker exec -i htmlpagegen_postgres_1 psql -U htmlpagegen -d ${TEST_PREFIX}htmlpagegen

# 3. Проверка восстановленных данных
RESTORED_TABLES=$(docker exec htmlpagegen_postgres_1 psql -U htmlpagegen -d ${TEST_PREFIX}htmlpagegen -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")

if [ "$RESTORED_TABLES" -gt 0 ]; then
    echo "✅ Database restore test: PASSED ($RESTORED_TABLES tables)"
else
    echo "❌ Database restore test: FAILED"
fi

# 4. Тестирование файлов проектов
TEST_EXTRACT_DIR="/tmp/${TEST_PREFIX}projects"
mkdir -p $TEST_EXTRACT_DIR
tar -xzf $BACKUP_PATH/projects.tar.gz -C $TEST_EXTRACT_DIR

if [ -d "$TEST_EXTRACT_DIR/var/lib/htmlpagegen/projects" ]; then
    PROJECT_COUNT=$(find $TEST_EXTRACT_DIR -name "*.json" | wc -l)
    echo "✅ Projects restore test: PASSED ($PROJECT_COUNT projects)"
else
    echo "❌ Projects restore test: FAILED"
fi

# 5. Очистка тестовых данных
docker exec htmlpagegen_postgres_1 dropdb ${TEST_PREFIX}htmlpagegen
rm -rf $TEST_EXTRACT_DIR

echo "Restore test completed"
```

### Аудит безопасности

#### Проверка уязвимостей

```bash
#!/bin/bash
# scripts/security-audit.sh

echo "🔒 Starting security audit..."

# 1. Проверка Docker образов
echo "Checking Docker images for vulnerabilities..."
docker scout cves htmlpagegen/backend:latest
docker scout cves htmlpagegen/frontend:latest

# 2. Проверка зависимостей Python
echo "Checking Python dependencies..."
cd backend
pip-audit

# 3. Проверка зависимостей Node.js
echo "Checking Node.js dependencies..."
cd ../frontend
npm audit

# 4. Проверка конфигурации SSL
echo "Checking SSL configuration..."
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com < /dev/null | openssl x509 -noout -dates

# 5. Проверка открытых портов
echo "Checking open ports..."
nmap -sT localhost

# 6. Проверка файловых разрешений
echo "Checking file permissions..."
find . -type f -perm 777 2>/dev/null

# 7. Проверка логов на подозрительную активность
echo "Checking for suspicious activity..."
grep -i "error\|fail\|attack" /var/log/nginx/access.log | tail -20

echo "🔒 Security audit completed"
```

### Оптимизация производительности

#### Анализ производительности

```bash
#!/bin/bash
# scripts/performance-analysis.sh

echo "📊 Performance Analysis Report"
echo "=============================="

# 1. Использование CPU
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//'

# 2. Использование памяти
echo "Memory Usage:"
free -h | grep Mem | awk '{print "Used: " $3 "/" $2 " (" $3/$2*100 "%)"}'

# 3. Дисковое пространство
echo "Disk Usage:"
df -h / | tail -1 | awk '{print "Used: " $3 "/" $2 " (" $5 ")"}'

# 4. Время отклика API
echo "API Response Times:"
for endpoint in /health /api/v1/projects /api/v1/generate; do
    time=$(curl -o /dev/null -s -w '%{time_total}' http://localhost:8000$endpoint)
    echo "$endpoint: ${time}s"
done

# 5. Размер логов
echo "Log Sizes:"
du -sh /var/log/htmlpagegen/* 2>/dev/null | sort -hr

# 6. Активные соединения
echo "Active Connections:"
netstat -an | grep :8000 | wc -l

# 7. Статистика базы данных
echo "Database Statistics:"
docker exec htmlpagegen_postgres_1 psql -U htmlpagegen -d htmlpagegen_prod -c "
SELECT
    'Connections' as metric, count(*) as value FROM pg_stat_activity
UNION ALL
SELECT
    'Database Size' as metric, pg_size_pretty(pg_database_size('htmlpagegen_prod')) as value
UNION ALL
SELECT
    'Total Tables' as metric, count(*)::text as value FROM information_schema.tables WHERE table_schema='public';
"
```

## Устранение неполадок

### Общие проблемы и решения

#### Высокое использование памяти

```bash
# Определение процесса, потребляющего больше всего памяти
ps aux --sort=-%mem | head -10

# Перезапуск сервисов с ограничением памяти
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Очистка кэша системы
sync && echo 3 > /proc/sys/vm/drop_caches
```

#### Медленная работа базы данных

```sql
-- Поиск медленных запросов
SELECT query, mean_time, rows, 100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Проверка блокировок
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

#### Проблемы с SSL сертификатами

```bash
# Проверка срока действия сертификата
openssl x509 -in ssl/fullchain.pem -noout -enddate

# Обновление Let's Encrypt сертификата
certbot renew --dry-run
certbot renew

# Перезагрузка Nginx
nginx -t && nginx -s reload
```

#### Проблемы с DeepSeek API

```bash
# Проверка доступности API
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.deepseek.com/v1/models

# Проверка лимитов
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
     https://api.deepseek.com/v1/usage

# Проверка истории запросов
grep "deepseek" /var/log/htmlpagegen/backend.log | tail -20
```

### Автоматизированные скрипты восстановления

#### Автоматическое восстановление сервисов

```bash
#!/bin/bash
# scripts/auto-recovery.sh

SERVICE_NAME=${1:-htmlpagegen}
MAX_RETRIES=3
RETRY_COUNT=0

check_service() {
    if curl -f http://localhost:3000/health > /dev/null 2>&1 && \
       curl -f http://localhost:8000/health > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

restart_service() {
    echo "Restarting $SERVICE_NAME..."
    docker-compose -f docker-compose.prod.yml restart
    sleep 30
}

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if check_service; then
        echo "✅ Service is healthy"
        exit 0
    else
        echo "❌ Service is unhealthy, attempting restart ($((RETRY_COUNT + 1))/$MAX_RETRIES)"
        restart_service
        RETRY_COUNT=$((RETRY_COUNT + 1))
    fi
done

echo "🚨 Failed to recover service after $MAX_RETRIES attempts"
# Отправка уведомления администратору
curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"🚨 HTMLpageGen service failed to recover automatically"}' \
    $SLACK_WEBHOOK_URL

exit 1
```

### Мониторинг и уведомления

#### Настройка Prometheus алертов

```yaml
# monitoring/alert-rules.yml
groups:
  - name: htmlpagegen
    rules:
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal - node_memory_MemAvailable) / node_memory_MemTotal > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"

      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"

      - alert: DeepSeekAPIError
        expr: increase(deepseek_api_errors_total[5m]) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate in DeepSeek API calls"
```

## Планирование обслуживания

### Календарь обслуживания

| Частота       | Операция                     | Время выполнения | Downtime  |
| ------------- | ---------------------------- | ---------------- | --------- |
| Ежедневно     | Health check                 | 5 минут          | Нет       |
| Еженедельно   | Обновление зависимостей      | 30 минут         | 2-5 минут |
| Ежемесячно    | Полное резервное копирование | 2 часа           | Нет       |
| Ежемесячно    | Оптимизация БД               | 1 час            | 10 минут  |
| Ежеквартально | Аудит безопасности           | 4 часа           | Нет       |
| Раз в полгода | Обновление ОС                | 2 часа           | 30 минут  |

### Окна обслуживания

```bash
# Уведомление пользователей о техническом обслуживании
curl -X POST http://localhost:8000/api/v1/maintenance \
    -H "Content-Type: application/json" \
    -d '{
        "start_time": "2025-02-01T02:00:00Z",
        "end_time": "2025-02-01T04:00:00Z",
        "message": "Плановое техническое обслуживание"
    }'

# Включение режима обслуживания
echo "maintenance" > /var/lib/htmlpagegen/status

# Выполнение обслуживания
./scripts/monthly-maintenance.sh

# Выключение режима обслуживания
rm /var/lib/htmlpagegen/status
```

---

_Регулярное обслуживание обеспечивает стабильную работу HTMLpageGen. Следуйте расписанию и документируйте все изменения._
