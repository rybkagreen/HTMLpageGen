# HTMLpageGen

HTML-генератор страниц - это инструмент для создания HTML-страниц с интеграцией искусственного интеллекта.

## Описание

Этот проект представляет собой веб-приложение для генерации HTML-страниц. Пользователи могут вводить текстовые описания, а приложение, используя модели OpenAI, генерирует соответствующий HTML-код.

## Структура проекта

-   **frontend**: Клиентская часть приложения, разработанная с использованием Next.js и React.
-   **backend**: Серверная часть, реализованная на FastAPI (Python), отвечает за бизнес-логику и взаимодействие с моделями OpenAI.
-   **shared**: Общая папка для файлов, которые могут использоваться как в frontend, так и в backend.
-   **.devcontainer**: Конфигурация для разработки в контейнерах Docker, обеспечивающая согласованную среду разработки.
-   **package.json**: Основной файл конфигурации проекта, содержащий скрипты для запуска и сборки приложения.

## Используемые технологии

-   **Frontend**:
    -   Next.js
    -   React
    -   TypeScript
    -   Tailwind CSS
-   **Backend**:
    -   FastAPI
    -   Python
    -   SQLAlchemy
    -   OpenAI API
-   **База данных**:
    -   PostgreSQL
-   **Контейнеризация**:
    -   Docker

## Краткая инструкция по запуску

1.  **Откройте проект в DevContainer (рекомендуется):**
    -   Используйте GitHub Codespaces для автоматической настройки окружения.
    -   Или откройте проект в VS Code с установленным расширением [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) и выполните команду `Dev Containers: Rebuild and Reopen in Container`.

2.  **Установите зависимости:**
    -   Выполните задачи `Install Frontend Dependencies` и `Install Backend Dependencies` через меню `Terminal > Run Task...`.

3.  **Запустите сервисы:**
    -   Запустите задачу `Start Docker Services` для старта базы данных и Redis.
    -   Запустите задачи `Start Frontend (Next.js)` и `Start Backend (FastAPI)` для старта серверов разработки.

4.  **Приложение будет доступно по адресу:**
    -   Frontend: `http://localhost:3000`
    -   Backend API: `http://localhost:8000/docs`

## Полезные ссылки

-   [Документация Next.js](https://nextjs.org/docs)
-   [Документация React](https://react.dev/)
-   [Документация FastAPI](https://fastapi.tiangolo.com/)
-   [Документация Docker](https://docs.docker.com/)
-   [Документация SQLAlchemy](https://www.sqlalchemy.org/docs/)
-   [Документация OpenAI API](https://beta.openai.com/docs/)
