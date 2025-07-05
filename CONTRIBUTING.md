# Руководство по внесению вклада в HTMLpageGen

Спасибо за интерес к развитию HTMLpageGen! Это руководство поможет вам начать участие в проекте.

## 🚀 Быстрый старт

### Настройка среды разработки

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/your-username/HTMLpageGen.git
   cd HTMLpageGen
   ```

2. **Используйте DevContainer (рекомендуется)**
   ```bash
   # Откройте в VS Code и выберите "Reopen in Container"
   code .
   ```

3. **Или настройте локально**
   ```bash
   # Backend
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

### Первый запуск

```bash
# В DevContainer или с настроенным окружением
docker-compose up -d --build

# Проверьте доступность
curl http://localhost:3000      # Frontend
curl http://localhost:8000/docs # Backend API docs
```

## 📋 Процесс разработки

### 1. Выбор задачи

- Изучите [Issues](https://github.com/your-username/HTMLpageGen/issues)
- Ищите метки `good first issue` для новичков
- Ищите метки `help wanted` для опытных разработчиков
- Комментируйте в Issue, что берете задачу в работу

### 2. Создание ветки

```bash
# Обновите main ветку
git checkout main
git pull origin main

# Создайте feature ветку
git checkout -b feature/issue-123-add-seo-module
# или
git checkout -b fix/issue-456-api-error-handling
```

**Именование веток:**
- `feature/issue-N-description` - новая функциональность
- `fix/issue-N-description` - исправление бага
- `docs/description` - изменения документации
- `refactor/description` - рефакторинг кода

### 3. Разработка

#### Стандарты кода

**Frontend (TypeScript/React):**
```typescript
// Используйте функциональные компоненты с TypeScript
interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: ReactNode;
  onClick?: () => void;
}

export const Button: FC<ButtonProps> = ({ variant, children, onClick }) => {
  return (
    <button
      className={cn('btn', `btn-${variant}`)}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

**Backend (Python/FastAPI):**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1", tags=["pages"])

@router.post("/pages", response_model=PageResponse)
async def create_page(
    page_data: PageCreate,
    db: Session = Depends(get_db)
) -> PageResponse:
    """
    Создает новую HTML страницу
    
    Args:
        page_data: Данные для создания страницы
        db: Сессия базы данных
        
    Returns:
        PageResponse: Созданная страница
    """
    try:
        # Бизнес-логика
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Тестирование

**Перед коммитом запустите:**
```bash
# Frontend
cd frontend
npm run lint
npm run type-check
npm run test
npm run build

# Backend
cd backend
flake8 app tests
mypy app
pytest tests/ -v
black --check app tests
```

### 4. Коммиты

**Формат коммитов:**
```
type(scope): краткое описание

Подробное описание изменений (если нужно)

- Что изменено
- Почему изменено
- Как это влияет на пользователей

Closes #123
```

**Типы коммитов:**
- `feat`: новая функциональность
- `fix`: исправление бага
- `docs`: изменения в документации
- `style`: форматирование, отступы
- `refactor`: рефакторинг кода
- `test`: добавление/изменение тестов
- `chore`: обновление зависимостей, конфигурации

**Примеры:**
```bash
git commit -m "feat(ai): add OpenAI integration for page generation

- Integrate OpenAI API for HTML generation
- Add error handling and retries
- Include comprehensive tests

Closes #45"

git commit -m "fix(api): handle validation errors correctly

- Return proper error messages for invalid input
- Add request validation middleware
- Update API documentation

Fixes #67"
```

### 5. Pull Request

#### Чеклист перед созданием PR

- [ ] Код протестирован и покрыт тестами
- [ ] Все проверки CI/CD проходят успешно
- [ ] Документация обновлена (если нужно)
- [ ] Нет конфликтов с main веткой
- [ ] Коммиты имеют понятные сообщения
- [ ] PR описание заполнено по шаблону

#### Шаблон PR

```markdown
## Описание изменений

Краткое описание того, что делает этот PR.

## Тип изменений

- [ ] 🐛 Bug fix (исправление, не меняющее API)
- [ ] ✨ New feature (новая функциональность)
- [ ] 💥 Breaking change (изменение, ломающее существующую функциональность)
- [ ] 📚 Documentation update (изменения документации)

## Связанные Issues

Closes #123
Related to #456

## Тестирование

Описание того, как были протестированы изменения:

- [ ] Unit тесты пройдены
- [ ] Integration тесты пройдены
- [ ] Мануальное тестирование выполнено
- [ ] Проверено в разных браузерах (если frontend)

## Скриншоты (если применимо)

![Before](image1.png)
![After](image2.png)

## Чеклист

- [ ] Код следует стандартам проекта
- [ ] Самостоятельный code review выполнен
- [ ] Документация обновлена
- [ ] Тесты добавлены/обновлены
- [ ] Все CI checks проходят
```

## 🧪 Тестирование

### Frontend тесты

```bash
# Unit тесты компонентов
npm run test

# E2E тесты
npm run test:e2e

# Тесты с покрытием
npm run test:coverage
```

**Пример теста компонента:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('should render with correct text', () => {
    render(<Button variant="primary">Test Button</Button>);
    expect(screen.getByText('Test Button')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = jest.fn();
    render(
      <Button variant="primary" onClick={handleClick}>
        Click me
      </Button>
    );
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Backend тесты

```bash
# Unit тесты
pytest tests/unit/ -v

# Integration тесты
pytest tests/integration/ -v

# Все тесты с покрытием
pytest tests/ -v --cov=app --cov-report=html
```

**Пример теста API:**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_page():
    response = client.post(
        "/api/v1/pages",
        json={
            "title": "Test Page",
            "description": "Create a test landing page",
            "style": "modern"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Page"
    assert "html_content" in data

def test_create_page_invalid_data():
    response = client.post(
        "/api/v1/pages",
        json={"title": ""}  # Пустой title
    )
    assert response.status_code == 422
```

## 📖 Документация

### Когда обновлять документацию

- При добавлении новых API endpoints
- При изменении существующего API
- При добавлении новых компонентов UI
- При изменении процесса установки/настройки

### Где документировать

- **API**: Обновите docstrings в коде + `/docs/api/`
- **Компоненты**: Комментарии в коде + Storybook
- **Гайды**: `/docs/guides/`
- **Архитектура**: `/docs/architecture/`

## 🔍 Code Review

### Что проверяем в Code Review

#### Общее
- [ ] Код читаемый и понятный
- [ ] Соблюдены стандарты проекта
- [ ] Нет дублирования кода
- [ ] Производительность не ухудшена
- [ ] Безопасность не нарушена

#### Frontend
- [ ] Компоненты переиспользуемы
- [ ] Состояние управляется корректно
- [ ] Accessibility соблюдено
- [ ] Responsive design работает
- [ ] Нет memory leaks

#### Backend
- [ ] API endpoints правильно спроектированы
- [ ] Валидация данных присутствует
- [ ] Ошибки обрабатываются корректно
- [ ] Database queries оптимизированы
- [ ] Безопасность (SQL injection, XSS и т.д.)

### Как давать feedback

**✅ Хорошо:**
```
Предлагаю использовать useMemo здесь для оптимизации:
```typescript
const expensiveValue = useMemo(() => calculateExpensiveValue(data), [data]);
```
Это предотвратит пересчеты при каждом рендере.
```

**❌ Плохо:**
```
Этот код плохой, перепиши.
```

## 🏷️ Релизы

### Semantic Versioning

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): Новая функциональность
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

### Процесс релиза

1. Создается release ветка от `develop`
2. Финальное тестирование и багфиксы
3. Обновляется CHANGELOG.md
4. Создается tag с версией
5. Merge в `main` и `develop`

## 🎯 Типы вкладов

### 🐛 Bug Reports

При создании bug report включите:
- Шаги для воспроизведения
- Ожидаемое поведение
- Фактическое поведение
- Версию браузера/Python
- Скриншоты (если применимо)

### ✨ Feature Requests

При предложении новой функциональности:
- Опишите проблему, которую решает фича
- Предложите решение
- Рассмотрите альтернативы
- Подумайте о влиянии на существующий код

### 📚 Документация

Улучшения документации всегда приветствуются:
- Исправление опечаток
- Улучшение примеров кода
- Добавление новых гайдов
- Переводы (планируется)

### 🧪 Тестирование

- Написание новых тестов
- Улучшение покрытия
- Performance тесты
- E2E тесты

## 📞 Получение помощи

### Где задать вопрос

- **GitHub Discussions** - общие вопросы о проекте
- **GitHub Issues** - баги и feature requests  
- **Email** - конфиденциальные вопросы
- **Slack** - быстрые вопросы (для core team)

### Менториство

Если вы новичок в разработке:
- Обращайтесь к мейнтейнерам за помощью
- Начинайте с `good first issue`
- Читайте код других контрибьюторов
- Не стесняйтесь задавать вопросы

## 🏆 Признание

Все контрибьюторы указываются в:
- README.md проекта
- Релизных нотах
- GitHub Contributors section

Особые вклады отмечаются в:
- Ежемесячных отчетах
- Социальных сетях проекта
- Конференциях и митапах

## 📄 Лицензия

Внося вклад в проект, вы соглашаетесь с тем, что ваш код будет лицензирован под [MIT License](LICENSE).

---

**Спасибо за ваш вклад в HTMLpageGen! 🚀**

Если у вас есть вопросы по этому руководству, создайте Issue или обратитесь к мейнтейнерам.
