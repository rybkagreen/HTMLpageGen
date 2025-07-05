'use client';

import { AnimatePresence, motion } from 'framer-motion';
import {
  Bot,
  Code,
  Copy,
  Download,
  Lightbulb,
  Loader2,
  Send,
  User,
} from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  reasoning?: string;
  generated_code?: {
    html: string;
    meta: any;
  };
}

interface ChatInterfaceProps {
  onCodeGenerated?: (html: string, meta: any) => void;
}

export default function ChatInterface({ onCodeGenerated }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content:
        'Привет! 👋 Я ваш персональный ИИ-агент для веб-разработки. Расскажите, что хотите создать, и я помогу вам воплотить идею в код.',
      timestamp: new Date(),
    },
  ]);

  const [inputMessage, setInputMessage] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [showReasoning, setShowReasoning] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isGenerating) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsGenerating(true);

    try {
      // Здесь будет запрос к DeepSeek R1 API
      const response = await fetch('/api/v1/chat/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputMessage,
          conversation_history: messages.slice(-5), // Последние 5 сообщений для контекста
        }),
      });

      if (!response.ok) throw new Error('Failed to generate response');

      const data = await response.json();

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.content,
        timestamp: new Date(),
        reasoning: data.reasoning,
        generated_code: data.generated_code,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Если сгенерирован код, передаем его наверх
      if (data.generated_code && onCodeGenerated) {
        onCodeGenerated(data.generated_code.html, data.generated_code.meta);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Извините, произошла ошибка. Попробуйте еще раз.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const downloadCode = (
    html: string,
    filename: string = 'generated-code.html'
  ) => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className='flex flex-col h-full bg-[#0D1117] text-white'>
      {/* Header */}
      <div className='flex items-center justify-between p-4 border-b border-gray-800'>
        <div className='flex items-center space-x-3'>
          <div className='w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center'>
            <Bot className='w-4 h-4 text-white' />
          </div>
          <div>
            <h3 className='text-sm font-semibold'>ИИ-Агент</h3>
            <p className='text-xs text-gray-400'>DeepSeek R1 • Онлайн</p>
          </div>
        </div>

        <div className='flex items-center space-x-2'>
          <button
            onClick={() => setShowReasoning(!showReasoning)}
            className={`p-2 rounded-lg transition-colors ${
              showReasoning
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
            title='Показать рассуждения ИИ'
          >
            <Lightbulb className='w-4 h-4' />
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
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`flex max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
              >
                {/* Avatar */}
                <div
                  className={`flex-shrink-0 ${message.role === 'user' ? 'ml-3' : 'mr-3'}`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      message.role === 'user'
                        ? 'bg-gray-700'
                        : 'bg-gradient-to-r from-blue-500 to-purple-500'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className='w-4 h-4 text-white' />
                    ) : (
                      <Bot className='w-4 h-4 text-white' />
                    )}
                  </div>
                </div>

                {/* Message Content */}
                <div
                  className={`flex flex-col space-y-2 ${message.role === 'user' ? 'items-end' : 'items-start'}`}
                >
                  <div
                    className={`px-4 py-3 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-800 text-gray-100'
                    }`}
                  >
                    <p className='text-sm whitespace-pre-wrap'>
                      {message.content}
                    </p>
                    <p className='text-xs mt-2 opacity-70'>
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>

                  {/* Reasoning Display */}
                  {message.reasoning && showReasoning && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className='bg-yellow-900/20 border border-yellow-600/30 rounded-lg p-3 text-sm'
                    >
                      <div className='flex items-center space-x-2 mb-2'>
                        <Lightbulb className='w-4 h-4 text-yellow-400' />
                        <span className='text-yellow-400 font-medium'>
                          Рассуждения ИИ:
                        </span>
                      </div>
                      <p className='text-gray-300 text-xs'>
                        {message.reasoning}
                      </p>
                    </motion.div>
                  )}

                  {/* Generated Code */}
                  {message.generated_code && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className='bg-gray-900 border border-gray-700 rounded-lg p-3 w-full'
                    >
                      <div className='flex items-center justify-between mb-2'>
                        <div className='flex items-center space-x-2'>
                          <Code className='w-4 h-4 text-green-400' />
                          <span className='text-green-400 font-medium text-sm'>
                            Сгенерированный код
                          </span>
                        </div>
                        <div className='flex items-center space-x-2'>
                          <button
                            onClick={() =>
                              copyToClipboard(message.generated_code!.html)
                            }
                            className='p-1 text-gray-400 hover:text-white transition-colors'
                            title='Копировать код'
                          >
                            <Copy className='w-4 h-4' />
                          </button>
                          <button
                            onClick={() =>
                              downloadCode(message.generated_code!.html)
                            }
                            className='p-1 text-gray-400 hover:text-white transition-colors'
                            title='Скачать файл'
                          >
                            <Download className='w-4 h-4' />
                          </button>
                        </div>
                      </div>
                      <div className='bg-black rounded p-2 overflow-x-auto'>
                        <pre className='text-xs text-gray-300'>
                          {message.generated_code.html.substring(0, 200)}
                          {message.generated_code.html.length > 200 && '...'}
                        </pre>
                      </div>
                    </motion.div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading */}
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className='flex justify-start'
          >
            <div className='flex items-center space-x-3'>
              <div className='w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center'>
                <Bot className='w-4 h-4 text-white' />
              </div>
              <div className='bg-gray-800 px-4 py-3 rounded-lg'>
                <div className='flex items-center space-x-2'>
                  <Loader2 className='w-4 h-4 animate-spin text-blue-400' />
                  <span className='text-sm text-gray-300'>
                    ИИ генерирует ответ...
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className='p-4 border-t border-gray-800'>
        <div className='flex items-end space-x-3'>
          <div className='flex-1 relative'>
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={e => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder='Опишите что хотите создать... (Enter для отправки, Shift+Enter для новой строки)'
              className='w-full max-h-32 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
              disabled={isGenerating}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isGenerating}
            className='p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors'
          >
            <Send className='w-4 h-4' />
          </button>
        </div>

        <div className='flex items-center justify-between mt-2 text-xs text-gray-500'>
          <span>Используйте естественный язык для описания ваших идей</span>
          <span>{inputMessage.length}/1000</span>
        </div>
      </div>
    </div>
  );
}
