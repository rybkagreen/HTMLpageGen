# Часто задаваемые вопросы (FAQ)

## Установка и настройка

### ❓ Какие минимальные системные требования?

**Ответ:** Минимальные требования:

- Node.js 18.0+
- Python 3.9+
- 4 GB RAM
- 2 GB свободного места

Рекомендуемые:

- Node.js 20.0+
- Python 3.11+
- 8 GB RAM
- 5 GB свободного места

### ❓ Нужен ли API ключ для работы?

**Ответ:** Да, для работы ИИ-генерации необходим API ключ DeepSeek. Получить его можно бесплатно на [platform.deepseek.com](https://platform.deepseek.com).

### ❓ Можно ли использовать без Docker?

**Ответ:** Да, можно установить локально. Docker рекомендуется для простоты развертывания, но не обязателен. См. [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md).

### ❓ Как обновить приложение?

**Ответ:**

```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### ❓ Поддерживаются ли другие ИИ модели?

**Ответ:** В настоящее время поддерживается только DeepSeek. Планируется добавление OpenAI GPT, Anthropic Claude в будущих версиях.

## Использование генератора

### ❓ Как написать эффективный промпт?

**Ответ:** Используйте конкретные описания:

```
✅ Хорошо: "Создай адаптивную карточку товара с изображением, названием, ценой и кнопкой покупки"
❌ Плохо: "Сделай красивую страницу"
```

### ❓ Какой максимальный размер генерируемого кода?

**Ответ:** По умолчанию лимит составляет 8000 токенов (~32KB кода). Можно изменить в настройках.

### ❓ Почему генерация занимает много времени?

**Ответ:** Возможные причины:

1. Сложный промпт требует больше времени
2. Высокая нагрузка на API DeepSeek
3. Медленное интернет-соединение
4. Достигнуты лимиты API

### ❓ Можно ли генерировать React/Vue компоненты?

**Ответ:** Базовая версия генерирует HTML/CSS/JS. Поддержка React/Vue планируется в будущих версиях.

### ❓ Поддерживаются ли CSS фреймворки?

**Ответ:** Да, поддерживаются:

- Tailwind CSS
- Bootstrap 5
- Bulma
- Пользовательские CSS фреймворки

## Редактор кода

### ❓ Какие возможности редактора доступны?

**Ответ:** Monaco Editor предоставляет:

- Подсветка синтаксиса
- Автодополнение
- Проверка ошибок
- Поиск и замена
- Множественный курсор
- Форматирование кода

### ❓ Как изменить тему редактора?

**Ответ:** В настройках приложения выберите светлую или темную тему. Редактор автоматически адаптируется.

### ❓ Поддерживается ли Emmet?

**Ответ:** Да, Emmet сокращения поддерживаются для HTML и CSS.

### ❓ Можно ли импортировать существующий код?

**Ответ:** Да, можно:

1. Скопировать код в редактор
2. Импортировать файлы через меню
3. Загрузить проект из файла

## Проекты и сохранение

### ❓ Где хранятся проекты?

**Ответ:**

- В режиме разработки: localStorage браузера
- В production: PostgreSQL база данных
- Планируется: облачное хранилище

### ❓ Можно ли экспортировать проекты?

**Ответ:** Да, доступны форматы:

- Отдельные файлы (HTML, CSS, JS)
- ZIP архив
- Один HTML файл со встроенными стилями
- JSON для восстановления проекта

### ❓ Есть ли ограничения на количество проектов?

**Ответ:** В локальной версии ограничений нет. В облачной версии будут тарифные планы.

### ❓ Поддерживается ли версионирование?

**Ответ:** Базовое версионирование есть (автосохранение). Полный Git-подобный контроль версий планируется.

## Чат и ИИ-агент

### ❓ Что можно спросить у ИИ-агента?

**Ответ:** ИИ-агент помогает с:

- Объяснением кода
- Отладкой ошибок
- Оптимизацией производительности
- Лучшими практиками
- Обучением веб-разработке

### ❓ Запоминает ли ИИ контекст беседы?

**Ответ:** Да, в рамках одной сессии. История очищается при перезагрузке страницы.

### ❓ Можно ли попросить ИИ изменить сгенерированный код?

**Ответ:** Да, например:

```
"Сделай эту кнопку больше и добавь тень"
"Измени цветовую схему на синюю"
"Добавь анимацию при наведении"
```

### ❓ Поддерживаются ли другие языки кроме русского?

**Ответ:** ИИ понимает английский, русский и другие языки. Интерфейс пока только на русском.

## Производительность и ограничения

### ❓ Сколько запросов в час можно делать?

**Ответ:** Зависит от лимитов вашего API ключа DeepSeek. Обычно:

- Бесплатный: 200 запросов/час
- Платный: без ограничений (по тарифу)

### ❓ Почему приложение медленно работает?

**Ответ:** Возможные причины:

1. Слабое железо (нужно минимум 4GB RAM)
2. Много открытых проектов
3. Большой размер генерируемого кода
4. Проблемы с интернетом

### ❓ Как очистить кэш?

**Ответ:**

```bash
# Очистка браузерного кэша
Ctrl+Shift+Delete

# Очистка серверного кэша
docker-compose restart redis
```

### ❓ Поддерживается ли оффлайн режим?

**Ответ:** Частично. Редактирование кода работает оффлайн, но ИИ-генерация требует интернет.

## Безопасность и приватность

### ❓ Сохраняются ли промпты на серверах DeepSeek?

**Ответ:** Согласно политике DeepSeek, данные могут временно сохраняться для улучшения модели. Не отправляйте конфиденциальную информацию.

### ❓ Можно ли использовать приватный ИИ?

**Ответ:** Планируется поддержка локальных моделей (Ollama, LM Studio) в будущих версиях.

### ❓ Как защищены пользовательские данные?

**Ответ:**

- HTTPS шифрование
- Хеширование паролей
- CORS защита
- Rate limiting
- Валидация входных данных

### ❓ Есть ли логирование действий пользователей?

**Ответ:** Логируются только технические события (ошибки, производительность). Содержимое проектов не логируется.

## Интеграции и API

### ❓ Есть ли API для внешних приложений?

**Ответ:** Да, REST API доступен на `/api/v1/`. Документация в [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

### ❓ Можно ли интегрировать с GitHub?

**Ответ:** Планируется. Пока доступен экспорт файлов для ручной загрузки в репозиторий.

### ❓ Поддерживается ли деплой на хостинг?

**Ответ:** Планируется интеграция с:

- Netlify
- Vercel
- GitHub Pages
- Custom webhooks

### ❓ Можно ли добавить пользовательские компоненты?

**Ответ:** В планах система плагинов для добавления:

- Пользовательских шаблонов
- Библиотек компонентов
- Кастомных ИИ-промптов

## Устранение неполадок

### ❓ Ошибка "DeepSeek API key not found"

**Ответ:**

1. Проверьте .env файлы
2. Убедитесь, что ключ активен
3. Проверьте формат ключа
4. Перезапустите приложение

### ❓ Ошибка "Failed to generate HTML"

**Ответ:**

1. Проверьте интернет-соединение
2. Упростите промпт
3. Проверьте лимиты API
4. Попробуйте через несколько минут

### ❓ Страница не отображается в предварительном просмотре

**Ответ:**

1. Проверьте консоль браузера (F12)
2. Убедитесь в корректности HTML
3. Проверьте CSS синтаксис
4. Отключите блокировщики рекламы

### ❓ Медленное автодополнение в редакторе

**Ответ:**

1. Закройте ненужные вкладки браузера
2. Уменьшите размер файла
3. Отключите ненужные расширения браузера
4. Увеличьте RAM

### ❓ Ошибка при сохранении проекта

**Ответ:**

1. Проверьте место на диске
2. Убедитесь в корректности названия
3. Проверьте права доступа
4. Попробуйте экспорт вместо сохранения

## Планы развития

### ❓ Какие функции планируются?

**Ответ:**

- **Q1 2025**: React/Vue компоненты, темплейты
- **Q2 2025**: Облачное хранилище, коллаборация
- **Q3 2025**: Локальные ИИ модели, плагины
- **Q4 2025**: Мобильное приложение, API v2

### ❓ Планируется ли мобильная версия?

**Ответ:** Да, адаптивная веб-версия работает на мобильных. Нативное приложение планируется на Q4 2025.

### ❓ Будет ли платная версия?

**Ответ:** Базовая функциональность останется бесплатной. Планируются премиум функции:

- Неограниченные проекты
- Приоритетная поддержка
- Дополнительные ИИ модели
- Облачное хранилище

### ❓ Можно ли участвовать в разработке?

**Ответ:** Да! Проект open source. См. [CONTRIBUTING.md](./CONTRIBUTING.md) для участия.

---

## Не нашли ответ?

1. **Документация**: Проверьте [USER_GUIDE.md](./USER_GUIDE.md)
2. **GitHub Issues**: Создайте issue с тегом `question`
3. **Сообщество**: Присоединяйтесь к Discord серверу
4. **Email поддержка**: support@htmlpagegen.dev

_FAQ обновляется на основе вопросов пользователей. Последнее обновление: Январь 2025_
