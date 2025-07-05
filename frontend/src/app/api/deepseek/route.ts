import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

interface DeepSeekMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface DeepSeekRequest {
  messages: DeepSeekMessage[];
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
}

export async function POST(req: NextRequest) {
  try {
    const {
      messages,
      stream = false,
      temperature = 0.7,
      max_tokens = 4096,
    }: DeepSeekRequest = await req.json();

    if (!process.env.DEEPSEEK_API_KEY) {
      return NextResponse.json(
        {
          success: false,
          message: 'DeepSeek API ключ не настроен',
        },
        { status: 500 }
      );
    }

    const response = await fetch(
      'https://api.deepseek.com/v1/chat/completions',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.DEEPSEEK_API_KEY}`,
        },
        body: JSON.stringify({
          model: 'deepseek-chat',
          messages,
          max_tokens,
          temperature,
          stream,
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage =
        errorData.error?.message || `HTTP ${response.status}`;

      console.error('DeepSeek API Error:', {
        status: response.status,
        statusText: response.statusText,
        error: errorData,
      });

      return NextResponse.json(
        {
          success: false,
          message: `DeepSeek API error: ${errorMessage}`,
          error: errorData,
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json({
      success: true,
      message: data.choices[0].message.content,
      usage: data.usage,
    });
  } catch (error: any) {
    console.error('DeepSeek API Error:', error);

    let errorMessage = 'Ошибка при запросе к DeepSeek';

    if (error.message?.includes('API key')) {
      errorMessage = 'Неверный API ключ DeepSeek. Проверьте ключ в .env.local';
    } else if (error.message?.includes('rate_limit')) {
      errorMessage =
        'Превышен лимит запросов DeepSeek (100/час). Попробуйте позже.';
    } else if (error.message?.includes('insufficient_quota')) {
      errorMessage =
        'Недостаточно квоты DeepSeek. Проверьте баланс на platform.deepseek.com';
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
