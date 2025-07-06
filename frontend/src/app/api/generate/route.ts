import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

interface GenerateRequest {
  title: string;
  content: string;
  template: string;
  style?: string;
  features?: string[];
  ai_enhance?: boolean;
}

export async function POST(req: NextRequest) {
  try {
    const {
      title,
      content,
      template,
      style = 'dark',
      features = [],
      ai_enhance = true,
    }: GenerateRequest = await req.json();

    if (!title.trim() || !content.trim()) {
      return NextResponse.json(
        {
          success: false,
          message: 'Название и содержимое обязательны',
        },
        { status: 400 }
      );
    }

    if (!process.env.HF_TOKEN) {
      return NextResponse.json(
        {
          success: false,
          message: 'Hugging Face токен не настроен',
        },
        { status: 500 }
      );
    }

    // Формируем промпт для генерации HTML
    const prompt = `Создай современную HTML страницу со следующими параметрами:

Название: ${title}
Содержимое: ${content}
Шаблон: ${template}
Стиль: ${style}
Особенности: ${features.join(', ')}
AI улучшения: ${ai_enhance ? 'включены' : 'отключены'}

Требования:
- Используй семантический HTML5
- Добавь адаптивный CSS с медиа-запросами
- Включи мета-теги для SEO
- Используй современные CSS практики (Flexbox/Grid)
- Добавь hover-эффекты и плавные переходы
- Оптимизируй для производительности
- Добавь базовые схемы микроразметки Schema.org

Верни только готовый HTML код без дополнительных комментариев.`;

    const startTime = Date.now();

    const response = await fetch(
      'https://router.huggingface.co/featherless-ai/v1/chat/completions',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.HF_TOKEN}`,
        },
        body: JSON.stringify({
          model: 'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B',
          messages: [
            {
              role: 'system',
              content:
                'Ты - эксперт веб-разработчик, специализирующийся на создании современных, красивых и SEO-оптимизированных HTML страниц. Всегда создавай полный, валидный HTML код.',
            },
            {
              role: 'user',
              content: prompt,
            },
          ],
          temperature: 0.7,
          max_tokens: 4096,
          stream: false,
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage =
        errorData.error?.message || `HTTP ${response.status}`;

      console.error('Hugging Face API Error:', {
        status: response.status,
        error: errorData,
      });

      return NextResponse.json(
        {
          success: false,
          message: `Hugging Face API error: ${errorMessage}`,
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    const generationTime = Date.now() - startTime;
    
    // Проверяем структуру ответа
    console.log('Hugging Face response:', JSON.stringify(data, null, 2));
    
    let htmlContent = '';
    if (data.choices && data.choices[0] && data.choices[0].message) {
      htmlContent = data.choices[0].message.content;
    } else if (data.content) {
      htmlContent = data.content;
    } else if (typeof data === 'string') {
      htmlContent = data;
    } else {
      throw new Error('Неизвестная структура ответа от API');
    }

    // Извлекаем мета-теги из сгенерированного HTML
    const titleMatch = htmlContent?.match(/<title[^>]*>([^<]+)<\/title>/i);
    const descMatch = htmlContent?.match(
      /<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"']+)["\'][^>]*>/i
    );
    const keywordsMatch = htmlContent?.match(
      /<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"']+)["\'][^>]*>/i
    );

    const wordCount = content.split(/\s+/).filter(Boolean).length;
    const seoScore = calculateSEOScore(htmlContent || '');

    return NextResponse.json({
      html: htmlContent,
      meta: {
        generation_time: generationTime,
        template_used: template,
        ai_enhanced: ai_enhance,
        seo_score: seoScore,
        word_count: wordCount,
        meta_tags: {
          title: titleMatch?.[1] || title,
          description: descMatch?.[1] || content.substring(0, 160),
          keywords: keywordsMatch?.[1] || features.join(', '),
        },
      },
      plugins_applied: features,
      generation_time: generationTime / 1000,
    });
  } catch (error: any) {
    console.error('HTML Generation Error:', error);

    let errorMessage = 'Ошибка при генерации HTML';

    if (error.message?.includes('API key') || error.message?.includes('token')) {
      errorMessage = 'Неверный Hugging Face токен. Проверьте токен в .env.local';
    } else if (error.message?.includes('rate_limit')) {
      errorMessage =
        'Превышен лимит запросов Hugging Face. Попробуйте позже.';
    } else if (error.message?.includes('insufficient_quota')) {
      errorMessage =
        'Недостаточно квоты Hugging Face. Проверьте баланс.';
    }

    return NextResponse.json(
      {
        success: false,
        message: errorMessage,
        error: error.message,
      },
      { status: 500 }
    );
  }
}

function calculateSEOScore(html: string): number {
  let score = 0;

  // Проверка наличия title
  if (html.includes('<title>')) score += 20;

  // Проверка meta description
  if (html.includes('name="description"')) score += 20;

  // Проверка h1
  if (html.includes('<h1>')) score += 15;

  // Проверка meta viewport
  if (html.includes('name="viewport"')) score += 15;

  // Проверка alt атрибутов
  if (html.includes('alt=')) score += 10;

  // Проверка семантических тегов
  const semanticTags = [
    '<header>',
    '<main>',
    '<section>',
    '<article>',
    '<aside>',
    '<footer>',
  ];
  const foundTags = semanticTags.filter(tag => html.includes(tag));
  score += Math.min(foundTags.length * 3, 15);

  // Проверка структурированных данных
  if (html.includes('itemscope') || html.includes('application/ld+json'))
    score += 5;

  return Math.min(score, 100);
}
