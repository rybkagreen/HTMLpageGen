# HTML Page Generator with AI

Интеллектуальный генератор HTML-страниц, использующий возможности искусственного интеллекта через Hugging Face API.

## 🚀 Особенности

- **AI-генерация**: Создание HTML-страниц с помощью модели DeepSeek-R1-Distill-Qwen-14B
- **Интерактивный чат**: Общение с AI для создания и улучшения кода
- **Управление проектами**: Сохранение, экспорт и импорт проектов
- **Предпросмотр в реальном времени**: Мгновенный просмотр результатов
- **SEO-оптимизация**: Автоматическая генерация мета-тегов
- **Адаптивный дизайн**: Современные CSS практики и responsive design

## 🛠 Технологии

- **Next.js 15** - React фреймворк
- **TypeScript** - Типизированный JavaScript
- **Tailwind CSS** - Utility-first CSS фреймворк
- **Framer Motion** - Анимации
- **Hugging Face API** - AI модель через featherless-ai роутер
- **Monaco Editor** - Редактор кода

## 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. Настройте переменные окружения:
```bash
cp .env.local.example .env.local
```

Обновите `.env.local` с вашим Hugging Face токеном:
```env
HF_TOKEN=your_hugging_face_token_here
```

4. Запустите проект:
```bash
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

## 🔧 Настройка Hugging Face API

1. Зарегистрируйтесь на [huggingface.co](https://huggingface.co/)
2. Перейдите в [настройки токенов](https://huggingface.co/settings/tokens)
3. Создайте новый токен с правами доступа к API
4. Скопируйте токен в файл `.env.local`

## 🧪 Тестирование API

Выполните тестовый запрос:
```bash
export HF_TOKEN=your_actual_token
node test-hf-api.js
```

Или протестируйте напрямую с помощью curl:
```bash
curl https://router.huggingface.co/featherless-ai/v1/chat/completions \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{
        "messages": [
            {
                "role": "user",
                "content": "Создай простую HTML страницу"
            }
        ],
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
        "stream": false
    }'
```

## 📖 Структура проекта

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API роуты
│   │   ├── huggingface/   # Hugging Face API
│   │   └── generate/      # Генерация HTML
│   ├── ai/                # AI чат страница
│   ├── generator/         # Генератор HTML
│   └── projects/          # Управление проектами
├── components/            # React компоненты
│   ├── ai/               # AI интерфейсы
│   ├── projects/         # Управление проектами
│   ├── generator/        # Генератор
│   └── ui/               # UI компоненты
└── lib/                  # Библиотеки
    ├── api.ts            # API функции
    ├── ai-agent.ts       # AI агент
    ├── project-manager.ts # Менеджер проектов
    └── utils.ts          # Утилиты
```

## 🎯 Возможности

### AI Чат (/ai)
- Интерактивное общение с DeepSeek R1
- Быстрые действия для создания страниц
- Автоматическое извлечение HTML кода
- Предпросмотр результатов

### Генератор HTML (/generator)
- Создание страниц по описанию
- Выбор шаблонов и стилей
- Живой предпросмотр
- Экспорт готового кода

### Управление проектами (/projects)
- Сохранение проектов локально
- Импорт/экспорт проектов
- Поиск и фильтрация
- Статистика использования

## 🔍 API Роуты

- `POST /api/huggingface` - Основной API для работы с AI
- `POST /api/generate` - Генерация HTML страниц

## 🚀 Сборка и деплой

```bash
# Сборка проекта
npm run build

# Запуск production сервера
npm start

# Линтинг
npm run lint

# Форматирование
npm run format
```

## 📝 Примеры использования

### Создание лендинга
```
Создай landing page для IT-компании с услугами веб-разработки, современным дизайном и формой обратной связи
```

### Портфолио
```
Создай портфолио веб-разработчика с разделами о навыках, проектах и контактах
```

### Корпоративный сайт
```
Создай корпоративный сайт консалтинговой компании с информацией об услугах и команде
```

## ⚡ Производительность

- Время генерации: < 5 секунд
- Поддержка стриминга ответов
- Edge Runtime для быстрых API ответов
- Оптимизированная сборка Next.js

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Проект распространяется под лицензией MIT. См. `LICENSE` для подробной информации.

## 🔗 Полезные ссылки

- [Hugging Face Documentation](https://huggingface.co/docs)
- [DeepSeek R1 Model](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
