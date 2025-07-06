import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

interface HuggingFaceMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface HuggingFaceRequest {
  messages: HuggingFaceMessage[];
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
    }: HuggingFaceRequest = await req.json();

    if (!process.env.HF_TOKEN) {
      return NextResponse.json(
        {
          success: false,
          message: 'Hugging Face токен не настроен',
        },
        { status: 500 }
      );
    }

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

      console.error('Hugging Face API Error:', {
        status: response.status,
        statusText: response.statusText,
        error: errorData,
      });

      return NextResponse.json(
        {
          success: false,
          message: `Hugging Face API error: ${errorMessage}`,
          error: errorData,
        },
        { status: response.status }
      );
    }

    if (stream) {
      // Обработка потокового ответа
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) {
        return NextResponse.json(
          {
            success: false,
            message: 'Ошибка при получении потокового ответа',
          },
          { status: 500 }
        );
      }

      const readableStream = new ReadableStream({
        async start(controller) {
          try {
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              
              const chunk = decoder.decode(value, { stream: true });
              controller.enqueue(new TextEncoder().encode(chunk));
            }
          } catch (error) {
            controller.error(error);
          } finally {
            controller.close();
          }
        },
      });

      return new Response(readableStream, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    } else {
      // Обработка обычного ответа
      const data = await response.json();
      return NextResponse.json({
        success: true,
        message: data.choices[0].message.content,
        usage: data.usage,
      });
    }
  } catch (error: any) {
    console.error('Hugging Face API Error:', error);

    let errorMessage = 'Ошибка при запросе к Hugging Face';

    if (error.message?.includes('API key') || error.message?.includes('token')) {
      errorMessage = 'Неверный Hugging Face токен. Проверьте токен в .env.local';
    } else if (error.message?.includes('rate_limit')) {
      errorMessage = 'Превышен лимит запросов. Попробуйте позже.';
    } else if (error.message?.includes('insufficient_quota')) {
      errorMessage = 'Недостаточно квоты. Проверьте баланс на Hugging Face.';
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
