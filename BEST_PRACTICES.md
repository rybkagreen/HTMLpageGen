# ✨ Лучшие практики HTMLPageGen

## 🎯 Эффективное использование ИИ

### 📝 Написание промптов

#### ✅ Хорошие примеры

```
Создай лендинг для IT-стартапа с:
- Современным минималистичным дизайном
- Темной цветовой схемой
- Адаптивной версткой
- Секциями: герой, услуги, команда, контакты
- Call-to-action кнопками
```

```
Сделай страницу портфолио веб-разработчика:
- Используй градиенты синего и фиолетового
- Добавь анимации при прокрутке
- Включи секции: обо мне, проекты, навыки, контакты
- Оптимизируй для SEO
```

#### ❌ Избегайте

```
Сделай сайт                    // Слишком общее
Создай что-нибудь красивое     // Неконкретно
Много текста и картинок        // Не структурировано
```

### 🧠 Оптимизация работы с ИИ

#### Структурируйте запросы

1. **Цель**: Что создаем (лендинг, блог, портфолио)
2. **Стиль**: Дизайн и цветовая схема
3. **Контент**: Основные секции и элементы
4. **Технические требования**: Адаптивность, SEO, производительность

#### Используйте контекст

- ИИ помнит предыдущие сообщения в чате
- Ссылайтесь на предыдущие генерации: "Как в прошлой странице, но..."
- Уточняйте и дорабатывайте: "Добавь еще анимации"

#### Экспериментируйте с параметрами

- **Температура 0.3-0.7**: Для консистентного кода
- **Температура 0.7-1.0**: Для креативных решений
- **Макс. токены**: 2000-4000 для полных страниц

## 🎨 Дизайн и UX

### 🌈 Цветовые схемы

#### Популярные комбинации

```css
/* Современный минимализм */
background: #0d1117;
primary: #2563eb;
secondary: #8b5cf6;
text: #f8fafc;

/* Корпоративный стиль */
background: #ffffff;
primary: #1f2937;
secondary: #3b82f6;
text: #374151;

/* Креативный дизайн */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
primary: #ff6b6b;
secondary: #4ecdc4;
text: #ffffff;
```

### 📱 Адаптивность

#### Обязательные breakpoints

```css
/* Mobile First */
@media (min-width: 640px) {
  /* sm */
}
@media (min-width: 768px) {
  /* md */
}
@media (min-width: 1024px) {
  /* lg */
}
@media (min-width: 1280px) {
  /* xl */
}
```

#### Гибкие элементы

- Используйте `rem` для шрифтов
- `%` или `vw/vh` для ширины/высоты
- Flexbox и Grid для layout
- `clamp()` для адаптивных размеров

### ⚡ Производительность

#### Оптимизация изображений

```html
<!-- Lazy loading -->
<img src="image.jpg" loading="lazy" alt="Описание" />

<!-- Responsive images -->
<img
  src="small.jpg"
  srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
  sizes="(max-width: 480px) 480px, (max-width: 800px) 800px, 1200px"
  alt="Описание"
/>

<!-- WebP с fallback -->
<picture>
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="Описание" />
</picture>
```

#### CSS оптимизация

```css
/* Критический CSS inline */
<style>
  .hero { display: flex; align-items: center; min-height: 100vh; }
</style>

/* Некритический CSS асинхронно */
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## 🔍 SEO Оптимизация

### 🏷️ Мета-теги

#### Базовый набор

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Основные мета-теги -->
    <title>Заголовок страницы (до 60 символов)</title>
    <meta name="description" content="Описание страницы (до 160 символов)" />
    <meta name="keywords" content="ключевые, слова, через, запятую" />

    <!-- Open Graph -->
    <meta property="og:title" content="Заголовок для соцсетей" />
    <meta property="og:description" content="Описание для соцсетей" />
    <meta property="og:image" content="https://example.com/image.jpg" />
    <meta property="og:url" content="https://example.com" />
    <meta property="og:type" content="website" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Заголовок для Twitter" />
    <meta name="twitter:description" content="Описание для Twitter" />
    <meta name="twitter:image" content="https://example.com/image.jpg" />
  </head>
</html>
```

### 🏗️ Семантическая разметка

```html
<!-- Структурированные данные -->
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Название сайта",
    "url": "https://example.com",
    "description": "Описание сайта"
  }
</script>

<!-- Семантические теги -->
<header role="banner">
  <nav role="navigation">
    <ul>
      <li><a href="#home">Главная</a></li>
      <li><a href="#about">О нас</a></li>
    </ul>
  </nav>
</header>

<main role="main">
  <article>
    <h1>Заголовок статьи</h1>
    <p>Содержимое...</p>
  </article>
</main>

<aside role="complementary">
  <h2>Боковая панель</h2>
</aside>

<footer role="contentinfo">
  <p>&copy; 2025 Компания</p>
</footer>
```

## 🔐 Безопасность

### 🛡️ Защита от XSS

```javascript
// Санитизация пользовательского контента
function sanitizeHTML(str) {
  const temp = document.createElement("div");
  temp.textContent = str;
  return temp.innerHTML;
}

// Использование
const userInput = sanitizeHTML(input);
```

### 🔒 CSP Headers

```html
<meta
  http-equiv="Content-Security-Policy"
  content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;"
/>
```

## 📊 Аналитика и мониторинг

### 📈 Google Analytics 4

```html
<!-- Global site tag (gtag.js) - Google Analytics -->
<script
  async
  src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"
></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", "GA_MEASUREMENT_ID");
</script>
```

### 🎯 Отслеживание событий

```javascript
// Отслеживание кликов по кнопкам
document.querySelectorAll(".cta-button").forEach((button) => {
  button.addEventListener("click", () => {
    gtag("event", "click", {
      event_category: "CTA",
      event_label: button.textContent,
      value: 1,
    });
  });
});

// Отслеживание скроллинга
let scrolled = false;
window.addEventListener("scroll", () => {
  if (!scrolled && window.scrollY > window.innerHeight * 0.5) {
    scrolled = true;
    gtag("event", "scroll", {
      event_category: "Engagement",
      event_label: "50% Page Scroll",
    });
  }
});
```

## 🧪 Тестирование

### ✅ Чек-лист перед публикацией

#### Функциональность

- [ ] Все ссылки работают
- [ ] Формы отправляются корректно
- [ ] Изображения загружаются
- [ ] Анимации плавные

#### Производительность

- [ ] PageSpeed Insights > 90
- [ ] Time to First Byte < 200ms
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1

#### SEO

- [ ] Title и description заполнены
- [ ] H1-H6 структурированы логически
- [ ] Alt теги для всех изображений
- [ ] robots.txt и sitemap.xml

#### Доступность

- [ ] Контрастность цветов >= 4.5:1
- [ ] Навигация с клавиатуры
- [ ] Screen reader friendly
- [ ] ARIA атрибуты где нужно

#### Кроссбраузерность

- [ ] Chrome (последняя версия)
- [ ] Firefox (последняя версия)
- [ ] Safari (iOS и macOS)
- [ ] Edge (последняя версия)

### 🔧 Инструменты тестирования

```bash
# Lighthouse CLI
npm install -g lighthouse
lighthouse https://example.com --output html --output-path ./report.html

# Accessibility testing
npm install -g @axe-core/cli
axe https://example.com

# Performance monitoring
npm install -g web-vitals-cli
web-vitals https://example.com
```

## 🚀 Деплой и продакшн

### 🏗️ Build оптимизация

```javascript
// next.config.js
module.exports = {
  output: "export",
  images: {
    unoptimized: true,
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === "production",
  },
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ["lucide-react", "framer-motion"],
  },
};
```

### 📦 CDN и кэширование

```html
<!-- Preload критических ресурсов -->
<link
  rel="preload"
  href="/fonts/font.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
<link rel="preload" href="/images/hero.jpg" as="image" />

<!-- DNS prefetch для внешних ресурсов -->
<link rel="dns-prefetch" href="//fonts.googleapis.com" />
<link rel="dns-prefetch" href="//www.google-analytics.com" />
```

### 🔄 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: "18"
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Build
        run: npm run build
      - name: Deploy
        run: npm run deploy
```

## 💡 Советы и трюки

### 🎨 CSS хаки

```css
/* Плавные скроллы */
html {
  scroll-behavior: smooth;
}

/* Убираем outline, но сохраняем для клавиатуры */
*:focus:not(.focus-visible) {
  outline: none;
}

/* Responsive typography */
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}

/* Aspect ratio для изображений */
.image-container {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

/* Градиенты с fallback */
.gradient-bg {
  background: #667eea; /* fallback */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### ⚡ JavaScript оптимизация

```javascript
// Debounce для скролла и ресайза
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

window.addEventListener(
  "scroll",
  debounce(() => {
    // Ваш код
  }, 100)
);

// Intersection Observer для lazy loading
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove("lazy");
      imageObserver.unobserve(img);
    }
  });
});

document.querySelectorAll("img[data-src]").forEach((img) => {
  imageObserver.observe(img);
});
```

---

**Следуя этим практикам, вы создадите высококачественные, производительные и SEO-оптимизированные веб-страницы! 🚀**
