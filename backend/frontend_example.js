/**
 * Примеры использования API структурированных данных во frontend
 */

// Конфигурация API
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Генерация структурированных данных
 */
async function generateStructuredData(content, schemaType, additionalData = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/generate-structured-data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: content,
                schema_type: schemaType,
                data: additionalData,
                auto_extract: true
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Ошибка генерации структурированных данных:', error);
        throw error;
    }
}

/**
 * Внедрение структурированных данных в HTML
 */
async function injectStructuredData(html, schemaTypes = null, autoDetect = true, schemaParams = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/inject-structured-data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                html: html,
                schema_types: schemaTypes,
                auto_detect: autoDetect,
                schema_params: schemaParams
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Ошибка внедрения структурированных данных:', error);
        throw error;
    }
}

/**
 * Генерация страницы со структурированными данными
 */
async function generatePageWithStructuredData(pageData) {
    try {
        const response = await fetch(`${API_BASE_URL}/pages/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pageData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Ошибка генерации страницы:', error);
        throw error;
    }
}

/**
 * Получение возможностей AI
 */
async function getAICapabilities() {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/capabilities`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const capabilities = await response.json();
        return capabilities;
    } catch (error) {
        console.error('Ошибка получения возможностей AI:', error);
        throw error;
    }
}

// Примеры использования

/**
 * Пример 1: Генерация FAQ схемы
 */
async function exampleFAQGeneration() {
    const content = `
        Что такое HTML генератор?
        HTML генератор — это инструмент для автоматического создания веб-страниц.
        
        Как использовать ИИ?
        Просто введите описание контента, и ИИ создаст HTML код.
        
        Поддерживается ли SEO?
        Да, генератор автоматически добавляет мета-теги и структурированные данные.
    `;

    try {
        const result = await generateStructuredData(content, 'faq', {
            name: 'Часто задаваемые вопросы о HTML генераторе',
            description: 'Ответы на популярные вопросы'
        });

        console.log('Сгенерированная FAQ схема:', result.schema_data);
        console.log('JSON-LD:', result.json_ld);
        
        return result;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

/**
 * Пример 2: Генерация страницы продукта
 */
async function exampleProductPage() {
    const pageData = {
        content: `
            Профессиональный HTML Генератор Pro
            
            Создавайте потрясающие веб-страницы с помощью искусственного интеллекта!
            
            Наш генератор использует передовые алгоритмы ИИ для создания 
            профессиональных HTML страниц за считанные секунды.
            
            Цена: 2999 рублей
            Бренд: WebGen Pro
            Артикул: HTMLGEN-PRO-2024
            
            Отзывы клиентов:
            ⭐⭐⭐⭐⭐ "Отличный инструмент!" - Иван П.
            ⭐⭐⭐⭐ "Хорошо, но есть что улучшить" - Мария С.
        `,
        template: 'default',
        structured_data: true,
        structured_data_types: ['product', 'organization'],
        structured_data_params: {
            product: {
                name: 'HTML Генератор Pro',
                brand: 'WebGen Pro',
                sku: 'HTMLGEN-PRO-2024',
                price: 2999,
                currency: 'RUB',
                url: 'https://example.com/html-generator-pro'
            },
            organization: {
                name: 'WebGen Technologies',
                url: 'https://webgen-tech.com'
            }
        }
    };

    try {
        const result = await generatePageWithStructuredData(pageData);
        
        console.log('Сгенерированная страница с метаданными:', result.meta);
        console.log('Информация о структурированных данных:', result.meta.structured_data);
        
        // Отображение HTML в iframe или контейнере
        const container = document.getElementById('preview-container');
        if (container) {
            container.innerHTML = result.html;
        }
        
        return result;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

/**
 * Пример 3: Автоматическое внедрение схем в существующий HTML
 */
async function exampleAutoInject() {
    const existingHTML = `
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <title>Мой блог</title>
        </head>
        <body>
            <nav>
                <a href="/">Главная</a> > 
                <a href="/blog">Блог</a> > 
                <span>Статья о веб-разработке</span>
            </nav>
            
            <article>
                <h1>Как создать современную веб-страницу</h1>
                <p>Автор: Алексей Разработчик</p>
                <p>Опубликовано: 20 января 2024</p>
                
                <p>В этой статье мы рассмотрим...</p>
                
                <h2>Часто задаваемые вопросы</h2>
                <h3>Что такое веб-разработка?</h3>
                <p>Веб-разработка — это процесс создания веб-сайтов.</p>
                
                <h3>Какие технологии используются?</h3>
                <p>HTML, CSS, JavaScript и многие другие.</p>
            </article>
        </body>
        </html>
    `;

    try {
        const result = await injectStructuredData(
            existingHTML,
            null, // Автоматическое определение типов схем
            true,  // Включить автодетект
            {}
        );

        console.log('HTML с внедренными схемами:', result.html);
        console.log('Добавлено схем:', result.schemas_added);
        console.log('Типы схем:', result.schemas_list);
        
        return result;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

/**
 * Пример 4: Создание интерактивного интерфейса
 */
function createStructuredDataInterface() {
    const container = document.createElement('div');
    container.innerHTML = `
        <div style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
            <h2>Генератор структурированных данных</h2>
            
            <div style="margin-bottom: 20px;">
                <label for="content-input">Контент:</label>
                <textarea id="content-input" rows="10" cols="80" 
                    placeholder="Введите контент для анализа..."
                    style="width: 100%; margin-top: 5px;"></textarea>
            </div>
            
            <div style="margin-bottom: 20px;">
                <label for="schema-select">Тип схемы:</label>
                <select id="schema-select" style="margin-left: 10px;">
                    <option value="auto">Автоопределение</option>
                    <option value="faq">FAQ</option>
                    <option value="product">Продукт</option>
                    <option value="article">Статья</option>
                    <option value="organization">Организация</option>
                    <option value="breadcrumb">Хлебные крошки</option>
                </select>
            </div>
            
            <button id="generate-btn" onclick="handleGenerate()" 
                style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                Генерировать схему
            </button>
            
            <div id="result-container" style="margin-top: 20px; display: none;">
                <h3>Результат:</h3>
                <pre id="result-output" style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;"></pre>
            </div>
            
            <div id="loading" style="display: none; margin-top: 20px;">
                <p>Генерация схемы... ⏳</p>
            </div>
        </div>
    `;

    // Добавляем обработчик
    window.handleGenerate = async function() {
        const content = document.getElementById('content-input').value;
        const schemaType = document.getElementById('schema-select').value;
        const loading = document.getElementById('loading');
        const resultContainer = document.getElementById('result-container');
        const resultOutput = document.getElementById('result-output');

        if (!content.trim()) {
            alert('Пожалуйста, введите контент для анализа');
            return;
        }

        loading.style.display = 'block';
        resultContainer.style.display = 'none';

        try {
            let result;
            
            if (schemaType === 'auto') {
                // Автоматическое внедрение
                const dummyHTML = `<html><body>${content}</body></html>`;
                result = await injectStructuredData(dummyHTML, null, true, {});
                resultOutput.textContent = JSON.stringify({
                    schemas_added: result.schemas_added,
                    schemas_list: result.schemas_list,
                    // Извлекаем JSON-LD из HTML
                    extracted_schemas: extractJSONLD(result.html)
                }, null, 2);
            } else {
                // Генерация конкретной схемы
                result = await generateStructuredData(content, schemaType);
                resultOutput.textContent = result.json_ld;
            }

            resultContainer.style.display = 'block';
        } catch (error) {
            alert('Ошибка генерации: ' + error.message);
        } finally {
            loading.style.display = 'none';
        }
    };

    return container;
}

/**
 * Извлечение JSON-LD из HTML
 */
function extractJSONLD(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const scripts = doc.querySelectorAll('script[type="application/ld+json"]');
    
    return Array.from(scripts).map(script => {
        try {
            return JSON.parse(script.textContent);
        } catch (e) {
            return script.textContent;
        }
    });
}

/**
 * Инициализация при загрузке страницы
 */
document.addEventListener('DOMContentLoaded', async function() {
    console.log('Инициализация интерфейса структурированных данных...');
    
    try {
        // Получаем возможности AI
        const capabilities = await getAICapabilities();
        console.log('Доступные возможности AI:', capabilities);
        
        // Можно показать доступные типы схем в интерфейсе
        if (capabilities.structured_data_types) {
            console.log('Поддерживаемые типы схем:', capabilities.structured_data_types);
        }
    } catch (error) {
        console.error('Ошибка инициализации:', error);
    }
});

// Экспорт функций для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        generateStructuredData,
        injectStructuredData,
        generatePageWithStructuredData,
        getAICapabilities,
        createStructuredDataInterface,
        extractJSONLD
    };
}
