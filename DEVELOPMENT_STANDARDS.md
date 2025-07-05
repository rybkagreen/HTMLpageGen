# 📖 Стандарты разработки HTMLpageGen

## Оглавление

1. [Общие принципы](#общие-принципы)
2. [Стандарт кода](#стандарт-кода)
3. [Стандарт документации](#стандарт-документации)
4. [Стандарт отчетности](#стандарт-отчетности)
5. [Правила линтинга](#правила-линтинга)
6. [Git Flow](#git-flow)
7. [Тестирование](#тестирование)

## Общие принципы

### Архитектурные принципы

1. **Разделение ответственности** - четкое разделение Frontend/Backend/Shared
2. **Модульность** - каждый модуль должен иметь одну ответственность
3. **Масштабируемость** - код должен легко расширяться
4. **Тестируемость** - каждый компонент должен быть покрыт тестами
5. **Документируемость** - весь код должен быть самодокументируемым

### Стек технологий

#### Frontend
- **Framework**: Next.js 15.x
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4.x
- **State Management**: React Context API / Zustand
- **Testing**: Jest + React Testing Library

#### Backend
- **Framework**: FastAPI 0.104.x
- **Language**: Python 3.11+
- **Database**: PostgreSQL + SQLAlchemy
- **Cache**: Redis
- **Testing**: pytest + pytest-asyncio

#### DevOps
- **Containerization**: Docker + Docker Compose
- **Development**: DevContainer
- **CI/CD**: GitHub Actions (планируется)

## Стандарт кода

### Общие правила

1. **Язык комментариев**: Русский для бизнес-логики, английский для технических деталей
2. **Именование**: 
   - Функции и переменные: camelCase (TS) / snake_case (Python)
   - Компоненты React: PascalCase
   - Константы: UPPER_SNAKE_CASE
   - Файлы: kebab-case для утилит, PascalCase для компонентов

### Frontend (TypeScript/React)

#### Структура файлов
```
src/
├── app/                    # App Router pages
├── components/             # Переиспользуемые компоненты
│   ├── ui/                # Base UI компоненты
│   ├── forms/             # Формы
│   └── layout/            # Layout компоненты
├── modules/               # Бизнес-модули
│   ├── ai-integration/    # AI интеграция
│   ├── page-generator/    # Генератор страниц
│   └── seo/               # SEO модуль
├── lib/                   # Утилиты и helpers
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript типы
└── constants/             # Константы
```

#### Стандарт компонентов
```typescript
// components/ui/Button.tsx
import { FC, ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

/**
 * Универсальная кнопка с поддержкой различных вариантов оформления
 */
export const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className,
}) => {
  return (
    <button
      className={cn(
        'rounded-lg font-medium transition-colors',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          'bg-red-600 text-white hover:bg-red-700': variant === 'danger',
        },
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        { 'opacity-50 cursor-not-allowed': disabled },
        className
      )}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

#### Стандарт хуков
```typescript
// hooks/useApiCall.ts
import { useState, useCallback } from 'react';

interface UseApiCallOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

/**
 * Хук для работы с API вызовами
 */
export const useApiCall = <T>(
  apiFunction: () => Promise<T>,
  options: UseApiCallOptions<T> = {}
) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiFunction();
      setData(result);
      options.onSuccess?.(result);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      options.onError?.(error);
    } finally {
      setLoading(false);
    }
  }, [apiFunction, options]);

  return { data, loading, error, execute };
};
```

### Backend (Python/FastAPI)

#### Структура файлов
```
app/
├── main.py                # Точка входа
├── core/                  # Основные настройки
│   ├── config.py         # Конфигурация
│   ├── database.py       # Подключение к БД
│   └── security.py       # Безопасность
├── api/                   # API endpoints
│   └── routes/           # Роуты по модулям
├── models/               # SQLAlchemy модели
├── schemas/              # Pydantic схемы
├── services/             # Бизнес-логика
├── modules/              # Специализированные модули
├── utils/                # Утилиты
└── tests/                # Тесты
```

#### Стандарт API endpoints
```python
# api/routes/pages.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.page import PageCreate, PageResponse
from app.services.page_generator import PageGeneratorService

router = APIRouter(prefix="/pages", tags=["pages"])

@router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page_data: PageCreate,
    db: Session = Depends(get_db)
) -> PageResponse:
    """
    Создает новую HTML страницу на основе пользовательского описания
    
    Args:
        page_data: Данные для создания страницы
        db: Сессия базы данных
        
    Returns:
        PageResponse: Созданная страница
        
    Raises:
        HTTPException: 400 если данные некорректны
        HTTPException: 500 при ошибке генерации
    """
    try:
        service = PageGeneratorService(db)
        page = await service.create_page(page_data)
        return PageResponse.from_orm(page)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании страницы"
        )
```

#### Стандарт сервисов
```python
# services/page_generator.py
from typing import List, Optional
from sqlalchemy.orm import Session
import logging

from app.models.page import Page
from app.schemas.page import PageCreate
from app.modules.ai_integration.service import AIService
from app.modules.seo.service import SEOService

logger = logging.getLogger(__name__)

class PageGeneratorService:
    """Сервис для генерации HTML страниц с использованием AI"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.seo_service = SEOService()
    
    async def create_page(self, page_data: PageCreate) -> Page:
        """
        Создает новую страницу с AI-генерацией контента
        
        Args:
            page_data: Данные для создания страницы
            
        Returns:
            Page: Созданная страница
            
        Raises:
            ValueError: При некорректных входных данных
            Exception: При ошибке генерации
        """
        logger.info(f"Создание страницы: {page_data.title}")
        
        try:
            # Генерация HTML контента
            html_content = await self.ai_service.generate_html(
                description=page_data.description,
                style=page_data.style
            )
            
            # SEO оптимизация
            seo_data = await self.seo_service.optimize_content(
                title=page_data.title,
                content=html_content
            )
            
            # Сохранение в БД
            page = Page(
                title=page_data.title,
                description=page_data.description,
                html_content=html_content,
                meta_title=seo_data.meta_title,
                meta_description=seo_data.meta_description,
                keywords=seo_data.keywords
            )
            
            self.db.add(page)
            self.db.commit()
            self.db.refresh(page)
            
            logger.info(f"Страница создана успешно: ID {page.id}")
            return page
            
        except Exception as e:
            logger.error(f"Ошибка создания страницы: {e}")
            self.db.rollback()
            raise
```

## Стандарт документации

### Структура документации

1. **README.md** - Основная документация проекта
2. **docs/** - Детальная документация по модулям
3. **CHANGELOG.md** - История изменений
4. **CONTRIBUTING.md** - Руководство для контрибьюторов
5. **API.md** - Документация API

### Шаблон README для модулей

```markdown
# Название модуля

## Описание
Краткое описание назначения модуля

## Установка
Инструкции по установке и настройке

## Использование
Примеры использования с кодом

## API Reference
Документация публичного API

## Тестирование
Как запустить тесты

## Вклад в разработку
Как внести вклад в модуль
```

### Стандарт комментариев

#### TypeScript
```typescript
/**
 * Описание функции на русском языке
 * 
 * @param param1 - Описание параметра
 * @param param2 - Описание параметра
 * @returns Описание возвращаемого значения
 * @throws {Error} Когда выбрасывается ошибка
 * 
 * @example
 * ```typescript
 * const result = myFunction('value1', 'value2');
 * ```
 */
```

#### Python
```python
def my_function(param1: str, param2: int) -> str:
    """
    Описание функции на русском языке
    
    Args:
        param1: Описание параметра
        param2: Описание параметра
        
    Returns:
        str: Описание возвращаемого значения
        
    Raises:
        ValueError: Когда выбрасывается ошибка
        
    Example:
        >>> result = my_function('value1', 42)
        >>> print(result)
        'expected_output'
    """
```

## Стандарт отчетности

### Структура отчетов

#### Еженедельный отчет разработки
```markdown
# Отчет о разработке - Неделя [ДД.ММ - ДД.ММ.ГГГГ]

## Выполненные задачи
- [ ] Задача 1 - краткое описание
- [ ] Задача 2 - краткое описание

## Метрики кода
- **Покрытие тестами**: XX%
- **Технический долг**: X часов
- **Новые bugs**: X
- **Исправленные bugs**: X

## Производительность
- **Frontend build time**: X минут
- **Backend response time**: X мс
- **Время загрузки страницы**: X сек

## Планы на следующую неделю
- Задача 1
- Задача 2

## Проблемы и риски
- Проблема 1 - план решения
- Риск 1 - план митигации
```

#### Отчет о тестировании
```markdown
# Отчет о тестировании - [ДД.ММ.ГГГГ]

## Общие метрики
- **Общее покрытие**: XX%
- **Unit тесты**: XX%
- **Integration тесты**: XX%
- **E2E тесты**: XX%

## Результаты по модулям
| Модуль | Покрытие | Пройдено | Упало | Статус |
|--------|----------|----------|-------|--------|
| Frontend/Components | XX% | XX | XX | ✅/❌ |
| Backend/API | XX% | XX | XX | ✅/❌ |
| AI Integration | XX% | XX | XX | ✅/❌ |

## Критические ошибки
- Ошибка 1 - описание и план исправления
- Ошибка 2 - описание и план исправления

## Рекомендации
- Рекомендация 1
- Рекомендация 2
```

### Шаблоны коммитов

```
type(scope): краткое описание изменений

Подробное описание изменений (если необходимо)

- Пункт 1
- Пункт 2

Closes #123
```

**Типы коммитов:**
- `feat`: новая функциональность
- `fix`: исправление ошибки
- `docs`: изменения в документации
- `style`: форматирование кода
- `refactor`: рефакторинг без изменения функциональности
- `test`: добавление или изменение тестов
- `chore`: обновление зависимостей, настроек

## Git Flow

### Ветки
- `main` - продакшен код
- `develop` - разработка
- `feature/[название]` - новая функциональность
- `fix/[название]` - исправления
- `release/[версия]` - подготовка релиза

### Процесс разработки
1. Создание feature ветки от `develop`
2. Разработка и тестирование
3. Pull Request в `develop`
4. Code Review
5. Merge после одобрения
6. Удаление feature ветки

## Тестирование

### Покрытие тестами
- **Минимальное покрытие**: 80%
- **Критические модули**: 95%+
- **Утилиты**: 90%+

### Типы тестов
1. **Unit тесты** - тестирование отдельных функций
2. **Integration тесты** - тестирование взаимодействия модулей
3. **E2E тесты** - тестирование пользовательских сценариев
4. **Performance тесты** - тестирование производительности

### Именование тестов
```typescript
describe('PageGenerator', () => {
  describe('createPage', () => {
    it('должен создать страницу с корректными данными', () => {
      // тест
    });
    
    it('должен выбросить ошибку при некорректных данных', () => {
      // тест
    });
  });
});
```

---

**Дата создания**: 03.07.2025  
**Версия**: 1.0.0  
**Ответственный**: Development Team
