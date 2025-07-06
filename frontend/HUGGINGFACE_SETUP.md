# Настройка Hugging Face API с DeepSeek R1

Этот проект использует **исключительно** Hugging Face API через featherless-ai роутер с моделью DeepSeek-R1-Distill-Qwen-14B.

## ✨ Что изменилось

- ❌ Удален DeepSeek API
- ✅ Только Hugging Face API
- ✅ Обновлены все API роуты
- ✅ Новый HuggingFaceAIPanel
- ✅ Улучшенная обработка ошибок

## 🚀 Быстрый старт

### 1. Получение токена Hugging Face

1. Зарегистрируйтесь на [huggingface.co](https://huggingface.co/)
2. Перейдите в [настройки токенов](https://huggingface.co/settings/tokens)
3. Создайте новый токен с правами доступа к API
4. Скопируйте токен

### 2. Настройка переменных окружения

Обновите файл `.env.local`:

```env
# Hugging Face API Configuration
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

### 3. Установка зависимостей

Если нужно, установите `node-fetch` для тестирования:

```bash
npm install node-fetch
```

## 🔧 API Конфигурация

### Используемое подключение

```bash
curl https://router.huggingface.co/featherless-ai/v1/chat/completions \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ],
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
        "stream": true
    }'
```

### Параметры API

- **URL**: `https://router.huggingface.co/featherless-ai/v1/chat/completions`
- **Модель**: `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B`
- **Авторизация**: Bearer токен Hugging Face
- **Поддержка стриминга**: Да
- **Максимальные токены**: 4096 (настраивается)

## 🧪 Тестирование

### Тест прямого API

```bash
export HF_TOKEN=your_actual_token
node test-hf-api.js
```

### Тест через веб-интерфейс

1. Запустите проект:
```bash
npm run dev
```

2. Откройте http://localhost:3000/ai

3. Используйте новый **HuggingFaceAIPanel** для:
   - AI чата с DeepSeek R1
   - Генерации HTML страниц
   - Предпросмотра результатов

## 📁 Структура файлов

### Новые файлы:

- `src/app/api/huggingface/route.ts` - API роут для Hugging Face
- `src/components/ai/HuggingFaceAIPanel.tsx` - Новый UI компонент
- `test-hf-api.js` - Скрипт тестирования
- `HUGGINGFACE_SETUP.md` - Эта документация

### Обновленные файлы:

- `.env.local` - Новые переменные окружения
- `src/app/ai/page.tsx` - Использует новый компонент

## 🎯 Возможности

### AI Чат
- Интерактивное общение с DeepSeek R1
- Быстрые действия для создания страниц
- Автоматическое извлечение HTML кода

### Генерация HTML
- Прямая генерация HTML по описанию
- Встроенные CSS стили
- Современные практики веб-разработки

### Предпросмотр
- Безопасный iframe для предпросмотра
- Возможность копирования кода
- Очистка результатов

## ⚡ Примеры использования

### Создание лендинга
```
Создай landing page для ресторана с меню, контактами и бронированием
```

### Портфолио
```
Создай портфолио веб-разработчика с проектами и навыками
```

### Корпоративный сайт
```
Создай корпоративный сайт IT-компании с услугами и командой
```

## 🔍 Возможные ошибки

### Ошибка токена
```
Hugging Face токен не настроен
```
**Решение**: Проверьте переменную `HF_TOKEN` в `.env.local`

### Ошибка API
```
HTTP 401 Unauthorized
```
**Решение**: Проверьте действительность токена на huggingface.co

### Превышение лимита
```
Превышен лимит запросов
```
**Решение**: Подождите или проверьте лимиты на Hugging Face

## 🚀 Производительность

- **Модель**: DeepSeek R1 - быстрая и качественная
- **Роутер**: featherless-ai - оптимизированный доступ
- **Стриминг**: Поддержка потоковых ответов
- **Кэширование**: Edge Runtime для быстрых ответов

## 🔄 Миграция с DeepSeek API

Если ранее использовался прямой DeepSeek API:

1. Замените `DEEPSEEK_API_KEY` на `HF_TOKEN`
2. Обновите компоненты для использования `HuggingFaceAIPanel`
3. Протестируйте новое подключение

## 📞 Поддержка

При возникновении проблем:

1. Проверьте токен Hugging Face
2. Убедитесь в наличии интернет-соединения
3. Проверьте логи в консоли браузера
4. Запустите тестовый скрипт `test-hf-api.js`

---

**Модель**: deepseek-ai/DeepSeek-R1-Distill-Qwen-14B  
**API**: Hugging Face Router (featherless-ai)  
**Статус**: Готов к использованию ✅
