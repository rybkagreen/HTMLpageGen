'use client';

import { cn } from '@/lib/utils';
import { AnimatePresence, motion } from 'framer-motion';
import { Bot, Copy, RefreshCw, Send, Sparkles, User } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { handleApiError, useErrorHandler } from '../ui/ErrorHandler';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  type?: 'text' | 'code' | 'html';
}

interface ChatInterfaceProps {
  onGenerateHTML?: (prompt: string) => void;
  className?: string;
}

export default function ChatInterface({
  onGenerateHTML,
  className,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content:
        'Привет! Я ИИ-ассистент для создания HTML-страниц. Опишите, что вы хотите создать, и я помогу вам!',
      timestamp: new Date(),
      type: 'text',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Обработка ошибок
  const { showError, ErrorComponent } = useErrorHandler();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
      type: 'text',
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/deepseek', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [
            {
              role: 'system',
              content:
                'Ты - эксперт веб-разработчик и дизайнер. Помогаешь пользователям создавать HTML-страницы. Если пользователь просит создать страницу, предложи конкретные детали: название, содержание, стиль. Отвечай на русском языке.',
            },
            ...messages
              .slice(-5)
              .map(m => ({ role: m.role, content: m.content })),
            { role: 'user', content: input },
          ],
        }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при запросе к ИИ');
      }

      const data = await response.json();

      if (data.success) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.message,
          timestamp: new Date(),
          type: 'text',
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error(data.message || 'Ошибка ИИ');
      }
    } catch (error: any) {
      console.error('Chat error:', error);

      // Показываем красивую ошибку
      handleApiError(error, showError);

      // Добавляем сообщение об ошибке в чат
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Извините, произошла ошибка. Попробуйте еще раз.',
        timestamp: new Date(),
        type: 'text',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div
      className={cn(
        'flex flex-col h-full bg-[#0D1117] border border-gray-700 rounded-lg',
        className
      )}
    >
      {/* Header */}
      <div className='flex items-center justify-between p-4 border-b border-gray-700'>
        <div className='flex items-center space-x-2'>
          <div className='w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center'>
            <Bot className='w-4 h-4 text-white' />
          </div>
          <div>
            <h3 className='font-semibold text-white'>ИИ Ассистент</h3>
            <p className='text-xs text-gray-400'>DeepSeek AI</p>
          </div>
        </div>

        <div className='flex items-center space-x-2'>
          <button
            onClick={() => setMessages(messages.slice(0, 1))}
            className='p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors'
            title='Очистить чат'
          >
            <RefreshCw className='w-4 h-4' />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className='flex-1 overflow-y-auto p-4 space-y-4'>
        <AnimatePresence>
          {messages.map(message => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className={cn(
                'flex items-start space-x-3',
                message.role === 'user'
                  ? 'flex-row-reverse space-x-reverse'
                  : ''
              )}
            >
              <div
                className={cn(
                  'w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0',
                  message.role === 'user'
                    ? 'bg-blue-600'
                    : 'bg-gradient-to-r from-purple-500 to-pink-500'
                )}
              >
                {message.role === 'user' ? (
                  <User className='w-4 h-4 text-white' />
                ) : (
                  <Sparkles className='w-4 h-4 text-white' />
                )}
              </div>

              <div
                className={cn(
                  'flex-1 max-w-[80%]',
                  message.role === 'user' ? 'text-right' : ''
                )}
              >
                <div
                  className={cn(
                    'inline-block p-3 rounded-lg',
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-100'
                  )}
                >
                  <div className='whitespace-pre-wrap break-words'>
                    {message.content}
                  </div>
                </div>

                <div className='flex items-center justify-between mt-1 px-1'>
                  <span className='text-xs text-gray-500'>
                    {message.timestamp.toLocaleTimeString()}
                  </span>

                  {message.role === 'assistant' && (
                    <button
                      onClick={() => copyToClipboard(message.content)}
                      className='p-1 text-gray-500 hover:text-gray-300 transition-colors'
                      title='Скопировать'
                    >
                      <Copy className='w-3 h-3' />
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className='flex items-start space-x-3'
          >
            <div className='w-8 h-8 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center'>
              <Sparkles className='w-4 h-4 text-white' />
            </div>
            <div className='bg-gray-800 p-3 rounded-lg'>
              <div className='flex space-x-2'>
                <div className='w-2 h-2 bg-gray-400 rounded-full animate-bounce' />
                <div className='w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100' />
                <div className='w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200' />
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className='p-4 border-t border-gray-700'>
        <div className='flex items-end space-x-2'>
          <div className='flex-1'>
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder='Опишите, что хотите создать...'
              className='w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none max-h-32 min-h-[2.5rem]'
              rows={1}
              disabled={isLoading}
            />
          </div>

          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className={cn(
              'p-2 rounded-lg transition-colors',
              !input.trim() || isLoading
                ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            )}
          >
            <Send className='w-4 h-4' />
          </button>
        </div>

        <div className='mt-2 text-xs text-gray-500'>
          Нажмите Enter для отправки, Shift+Enter для новой строки
        </div>
      </div>

      {/* Error Handler */}
      <ErrorComponent />
    </div>
  );
}
