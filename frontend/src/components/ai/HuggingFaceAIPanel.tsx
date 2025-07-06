'use client';

import { useState } from 'react';

interface HuggingFaceMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface HuggingFaceAPIResponse {
  success: boolean;
  message?: string;
  error?: string;
  usage?: any;
}

export default function HuggingFaceAIPanel() {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<HuggingFaceMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [generatedHTML, setGeneratedHTML] = useState('');
  const [activeTab, setActiveTab] = useState('chat');

  const sendMessageToHuggingFace = async (
    messages: HuggingFaceMessage[],
    options?: {
      stream?: boolean;
      temperature?: number;
      max_tokens?: number;
    }
  ): Promise<string> => {
    const response = await fetch('/api/huggingface', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages.map(m => ({ role: m.role, content: m.content })),
        stream: options?.stream || false,
        temperature: options?.temperature || 0.7,
        max_tokens: options?.max_tokens || 4096,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Ошибка API');
    }

    const data: HuggingFaceAPIResponse = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'Неизвестная ошибка');
    }

    return data.message || '';
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;

    const userMessage: HuggingFaceMessage = {
      role: 'user',
      content: currentMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      // Добавляем системное сообщение для лучшего контекста
      const systemMessage: HuggingFaceMessage = {
        role: 'system',
        content: 'Ты опытный веб-разработчик и дизайнер. Помогай создавать качественный HTML, CSS и JavaScript код. Отвечай на русском языке.',
        timestamp: new Date(),
      };

      const conversationMessages = [systemMessage, ...messages.slice(-5), userMessage];
      
      const response = await sendMessageToHuggingFace(conversationMessages);

      const assistantMessage: HuggingFaceMessage = {
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Если ответ содержит HTML код, извлекаем его
      const htmlMatch = response.match(/```html\n([\s\S]*?)\n```/);
      if (htmlMatch) {
        setGeneratedHTML(htmlMatch[1]);
      }

    } catch (error: any) {
      console.error('Chat error:', error);
      const errorMessage: HuggingFaceMessage = {
        role: 'assistant',
        content: `Извините, произошла ошибка: ${error.message}. Проверьте настройки API в .env.local файле.`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (prompt: string) => {
    setCurrentMessage(prompt);
  };

  const generateHTML = async (prompt: string) => {
    setLoading(true);
    try {
      const systemMessage: HuggingFaceMessage = {
        role: 'system',
        content: 'Ты эксперт по созданию современного HTML/CSS кода. Создавай чистый, семантический HTML с встроенными стилями CSS. Используй современные практики веб-разработки.',
        timestamp: new Date(),
      };

      const userMessage: HuggingFaceMessage = {
        role: 'user',
        content: `Создай HTML страницу: ${prompt}. Включи все необходимые стили CSS внутри тега <style>. Сделай дизайн современным и адаптивным.`,
        timestamp: new Date(),
      };

      const response = await sendMessageToHuggingFace([systemMessage, userMessage]);
      
      // Извлекаем HTML код из ответа
      const htmlMatch = response.match(/```html\n([\s\S]*?)\n```/);
      if (htmlMatch) {
        setGeneratedHTML(htmlMatch[1]);
      } else {
        setGeneratedHTML(response);
      }

    } catch (error: any) {
      console.error('HTML generation error:', error);
      alert(`Ошибка генерации: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'chat', label: 'AI Чат' },
    { id: 'generate', label: 'Генерация HTML' },
    { id: 'preview', label: 'Предпросмотр' },
  ];

  const quickActions = [
    'Создай landing page для ресторана',
    'Создай портфолио веб-разработчика',
    'Создай страницу контактов с формой',
    'Создай блог с несколькими статьями',
    'Создай интернет-магазин товаров',
    'Создай корпоративный сайт компании',
  ];

  return (
    <div className='bg-white rounded-lg shadow-lg p-6'>
      <div className='mb-6'>
        <h2 className='text-2xl font-bold text-gray-900 mb-2'>
          DeepSeek R1 AI Панель
        </h2>
        <p className='text-gray-600 text-sm'>
          Модель: deepseek-ai/DeepSeek-R1-Distill-Qwen-14B через Hugging Face
        </p>
      </div>

      {/* Tabs */}
      <div className='border-b border-gray-200 mb-6'>
        <nav className='flex space-x-8'>
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Chat Tab */}
      {activeTab === 'chat' && (
        <div className='space-y-4'>
          {/* Quick Actions */}
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Быстрые действия
            </label>
            <div className='grid grid-cols-1 md:grid-cols-2 gap-2'>
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickAction(action)}
                  disabled={loading}
                  className='bg-green-600 text-white px-3 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 text-sm text-left'
                >
                  {action}
                </button>
              ))}
            </div>
          </div>

          {/* Chat Messages */}
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Разговор с DeepSeek R1
            </label>
            <div className='border border-gray-300 rounded-md h-96 overflow-y-auto p-3 bg-gray-50'>
              {messages.length === 0 ? (
                <div className='text-gray-500 text-center py-8'>
                  <p>Начните разговор с AI помощником</p>
                  <p className='text-sm mt-1'>
                    Попробуйте быстрые действия выше или напишите свой запрос
                  </p>
                </div>
              ) : (
                <div className='space-y-3'>
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${
                        message.role === 'user'
                          ? 'justify-end'
                          : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-3 py-2 rounded-lg ${
                          message.role === 'user'
                            ? 'bg-blue-600 text-white'
                            : 'bg-white border text-gray-900'
                        }`}
                      >
                        <p className='text-sm whitespace-pre-wrap'>{message.content}</p>
                        <p className='text-xs mt-1 opacity-70'>
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                  {loading && (
                    <div className='flex justify-start'>
                      <div className='bg-white border px-3 py-2 rounded-lg'>
                        <div className='flex items-center space-x-1'>
                          <div className='w-2 h-2 bg-blue-400 rounded-full animate-bounce'></div>
                          <div
                            className='w-2 h-2 bg-blue-400 rounded-full animate-bounce'
                            style={{ animationDelay: '0.1s' }}
                          ></div>
                          <div
                            className='w-2 h-2 bg-blue-400 rounded-full animate-bounce'
                            style={{ animationDelay: '0.2s' }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Message Input */}
          <div className='flex space-x-2'>
            <input
              type='text'
              value={currentMessage}
              onChange={e => setCurrentMessage(e.target.value)}
              onKeyPress={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder='Опишите, что хотите создать...'
              className='flex-1 border border-gray-300 rounded-md px-3 py-2'
              disabled={loading}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !currentMessage.trim()}
              className='bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50'
            >
              {loading ? '...' : 'Отправить'}
            </button>
          </div>
        </div>
      )}

      {/* Generate Tab */}
      {activeTab === 'generate' && (
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Прямая генерация HTML
            </label>
            <textarea
              value={currentMessage}
              onChange={e => setCurrentMessage(e.target.value)}
              rows={4}
              className='w-full border border-gray-300 rounded-md px-3 py-2'
              placeholder='Опишите детально, какую HTML страницу вы хотите создать...'
            />
          </div>
          
          <button
            onClick={() => generateHTML(currentMessage)}
            disabled={loading || !currentMessage.trim()}
            className='bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50'
          >
            {loading ? 'Генерация...' : 'Сгенерировать HTML'}
          </button>

          {generatedHTML && (
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Сгенерированный HTML код
              </label>
              <textarea
                value={generatedHTML}
                readOnly
                rows={12}
                className='w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 font-mono text-sm'
              />
              <div className='mt-2 flex space-x-2'>
                <button
                  onClick={() => navigator.clipboard.writeText(generatedHTML)}
                  className='bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700'
                >
                  Копировать код
                </button>
                <button
                  onClick={() => setActiveTab('preview')}
                  className='bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700'
                >
                  Показать предпросмотр
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Preview Tab */}
      {activeTab === 'preview' && (
        <div className='space-y-4'>
          <div className='flex justify-between items-center'>
            <label className='block text-sm font-medium text-gray-700'>
              Предпросмотр HTML
            </label>
            <button
              onClick={() => setGeneratedHTML('')}
              className='bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700'
            >
              Очистить
            </button>
          </div>
          
          {generatedHTML ? (
            <div className='border border-gray-300 rounded-md overflow-hidden'>
              <iframe
                srcDoc={generatedHTML}
                className='w-full h-96'
                title='HTML Preview'
                sandbox='allow-same-origin'
              />
            </div>
          ) : (
            <div className='border border-gray-300 rounded-md h-96 flex items-center justify-center bg-gray-50'>
              <p className='text-gray-500'>
                Сгенерируйте HTML код для предпросмотра
              </p>
            </div>
          )}
        </div>
      )}

      {/* API Info */}
      <div className='mt-6 bg-blue-50 p-4 rounded-md'>
        <h4 className='text-sm font-medium text-blue-900 mb-2'>
          Информация о подключении:
        </h4>
        <ul className='text-xs text-blue-800 space-y-1'>
          <li>• API: Hugging Face Router (featherless-ai)</li>
          <li>• Модель: deepseek-ai/DeepSeek-R1-Distill-Qwen-14B</li>
          <li>• Поддержка: Создание HTML, CSS, JavaScript</li>
          <li>• Язык: Русский и английский</li>
        </ul>
      </div>
    </div>
  );
}
