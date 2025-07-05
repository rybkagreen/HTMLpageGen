'use client';

import { useEffect, useState } from 'react';

import { AIAgent, ConversationContext } from '@/lib/ai-agent';
import {
  enhanceContentAdvanced,
  generateHTMLContent,
  generateMetaTagsAdvanced,
  getImprovementSuggestions,
  getProviderInfo,
} from '@/lib/api';
import {
  ContentEnhancementRequest,
  HTMLGenerationRequest,
  ImprovementSuggestionRequest,
  MetaTagsRequest,
  ProviderInfoResponse,
} from '@/lib/types';
import { APIKeyManager, APIKeySettings } from './APIKeyManager';

export default function DeepSeekAIPanel() {
  const [activeTab, setActiveTab] = useState('settings');
  const [loading, setLoading] = useState(false);
  const [providerInfo, setProviderInfo] = useState<ProviderInfoResponse | null>(
    null
  );

  // Content Enhancement State
  const [content, setContent] = useState('');
  const [enhancementType, setEnhancementType] = useState('general');
  const [enhancedContent, setEnhancedContent] = useState('');

  // HTML Generation State
  const [prompt, setPrompt] = useState('');
  const [contentType, setContentType] = useState('webpage');
  const [generatedHTML, setGeneratedHTML] = useState('');

  // Meta Tags State
  const [metaContent, setMetaContent] = useState('');
  const [metaTags, setMetaTags] = useState({
    title: '',
    description: '',
    keywords: '',
  });

  // Improvements State
  const [htmlForAnalysis, setHtmlForAnalysis] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);

  // AI Agent State
  const [aiAgent, setAiAgent] = useState<AIAgent | null>(null);
  const [chatMessages, setChatMessages] = useState<
    Array<{
      role: 'user' | 'assistant';
      content: string;
      timestamp: Date;
    }>
  >([]);
  const [currentMessage, setCurrentMessage] = useState('');

  // API Settings State
  const [apiSettings, setApiSettings] = useState<APIKeySettings>({
    huggingfaceKey: '',
    useDirectClient: true,
  });

  const loadProviderInfo = async () => {
    try {
      const info = await getProviderInfo();
      setProviderInfo(info);
    } catch (error) {
      console.error('Failed to load provider info:', error);
    }
  };

  const handleEnhanceContent = async () => {
    if (!content.trim()) return;

    setLoading(true);
    try {
      const request: ContentEnhancementRequest = {
        content,
        enhancement_type: enhancementType,
      };
      const response = await enhanceContentAdvanced(request);
      setEnhancedContent(response.enhanced_content);
    } catch (error) {
      console.error('Failed to enhance content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateHTML = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const request: HTMLGenerationRequest = {
        prompt,
        content_type: contentType,
      };
      const response = await generateHTMLContent(request);
      setGeneratedHTML(response.html_content);
    } catch (error) {
      console.error('Failed to generate HTML:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateMetaTags = async () => {
    if (!metaContent.trim()) return;

    setLoading(true);
    try {
      const request: MetaTagsRequest = {
        content: metaContent,
      };
      const response = await generateMetaTagsAdvanced(request);
      setMetaTags(response);
    } catch (error) {
      console.error('Failed to generate meta tags:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeHTML = async () => {
    if (!htmlForAnalysis.trim()) return;

    setLoading(true);
    try {
      const request: ImprovementSuggestionRequest = {
        html: htmlForAnalysis,
      };
      const response = await getImprovementSuggestions(request);
      setSuggestions(response.suggestions);
    } catch (error) {
      console.error('Failed to analyze HTML:', error);
    } finally {
      setLoading(false);
    }
  };

  // Initialize AI Agent
  useEffect(() => {
    const context: ConversationContext = {
      messages: [],
      userPreferences: {
        preferredFrameworks: ['html', 'css', 'javascript'],
        designStyle: 'современный',
        complexity: 'medium',
      },
      sessionGoals: ['create_html_pages'],
    };
    setAiAgent(new AIAgent(context));
  }, []);

  useEffect(() => {
    loadProviderInfo();
  }, []);

  const tabs = [
    { id: 'settings', label: 'Настройки' },
    { id: 'chat', label: 'AI Чат' },
    { id: 'enhance', label: 'Улучшение контента' },
    { id: 'generate', label: 'Генерация HTML' },
    { id: 'meta', label: 'Мета-теги' },
    { id: 'analyze', label: 'Анализ HTML' },
  ];

  const enhancementTypes = [
    { value: 'general', label: 'Общее улучшение' },
    { value: 'seo', label: 'SEO оптимизация' },
    { value: 'accessibility', label: 'Доступность' },
    { value: 'marketing', label: 'Маркетинг' },
  ];

  const contentTypes = [
    { value: 'webpage', label: 'Веб-страница' },
    { value: 'landing', label: 'Лендинг' },
    { value: 'blog', label: 'Блог статья' },
    { value: 'portfolio', label: 'Портфолио' },
  ];

  // AI Agent Methods
  const handleSendMessage = async () => {
    if (!currentMessage.trim() || !aiAgent) return;

    const userMessage = {
      role: 'user' as const,
      content: currentMessage,
      timestamp: new Date(),
    };

    setChatMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      let response = '';

      // Используем прямой клиент если настроен API ключ
      if (apiSettings.useDirectClient && apiSettings.huggingfaceKey) {
        // Analyze requirements with AI
        const analysis =
          await aiAgent.analyzeRequirementsWithAI(currentMessage);

        // Handle different intents with direct client
        switch (analysis.intent) {
          case 'create_page':
            response = await aiAgent.generateWithDeepSeekDirect(
              apiSettings.huggingfaceKey,
              currentMessage,
              {
                contentType: analysis.contentType,
                complexity: analysis.complexity,
                style: analysis.designStyle,
              }
            );
            setGeneratedHTML(response);
            response = `Создал ${analysis.contentType} в стиле "${analysis.designStyle}". Код добавлен в редактор.`;
            break;

          case 'modify_page':
            response = await aiAgent.enhanceContentWithDeepSeekDirect(
              apiSettings.huggingfaceKey,
              generatedHTML || content,
              analysis.designStyle
            );
            setEnhancedContent(response);
            response = 'Улучшил содержимое страницы. Проверьте результат.';
            break;

          case 'analyze_code':
            const suggestions = await aiAgent.analyzeCodeWithDeepSeekDirect(
              apiSettings.huggingfaceKey,
              htmlForAnalysis || generatedHTML
            );
            setSuggestions(suggestions);
            response = `Анализ завершен. Найдено ${suggestions.length} рекомендаций.`;
            break;

          default:
            response = await aiAgent.chatWithDeepSeekDirect(
              apiSettings.huggingfaceKey,
              [...chatMessages.slice(-5), userMessage]
            );
        }
      } else {
        // Fallback к backend API
        const analysis =
          await aiAgent.analyzeRequirementsWithAI(currentMessage);

        // Handle different intents
        switch (analysis.intent) {
          case 'create_page':
            response = await aiAgent.generateWithDeepSeek(currentMessage, {
              contentType: analysis.contentType,
              complexity: analysis.complexity,
              style: analysis.designStyle,
            });
            setGeneratedHTML(response);
            response = `Создал ${analysis.contentType} в стиле "${analysis.designStyle}". Код добавлен в редактор.`;
            break;

          case 'modify_page':
            response = await aiAgent.enhanceContentWithDeepSeek(
              generatedHTML || content,
              analysis.designStyle
            );
            setEnhancedContent(response);
            response = 'Улучшил содержимое страницы. Проверьте результат.';
            break;

          case 'analyze_code':
            const suggestions = await aiAgent.analyzeCodeWithDeepSeek(
              htmlForAnalysis || generatedHTML
            );
            setSuggestions(suggestions);
            response = `Анализ завершен. Найдено ${suggestions.length} рекомендаций.`;
            break;

          default:
            response = await aiAgent.chatWithDeepSeek([
              ...chatMessages.slice(-5),
              userMessage,
            ]);
        }
      }

      const assistantMessage = {
        role: 'assistant' as const,
        content: response,
        timestamp: new Date(),
      };

      setChatMessages(prev => [...prev, assistantMessage]);
      aiAgent.updateContext(response, 'assistant');
    } catch (error) {
      console.error('AI chat error:', error);
      const errorMessage = {
        role: 'assistant' as const,
        content:
          'Извините, произошла ошибка при обработке запроса. Проверьте настройки AI провайдера.',
        timestamp: new Date(),
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = async (action: string) => {
    if (!aiAgent) return;

    setLoading(true);
    try {
      switch (action) {
        case 'generate_landing':
          setCurrentMessage('Создай современную landing-страницу для стартапа');
          break;
        case 'improve_seo':
          if (content || generatedHTML) {
            const tags = await aiAgent.generateSEOWithDeepSeek(
              content || generatedHTML
            );
            setMetaTags(tags);
            setCurrentMessage('Улучшите SEO оптимизацию страницы');
          }
          break;
        case 'analyze_performance':
          setCurrentMessage(
            'Проанализируй производительность и дай рекомендации'
          );
          break;
        case 'make_responsive':
          setCurrentMessage('Сделай дизайн адаптивным для мобильных устройств');
          break;
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='bg-white rounded-lg shadow-lg p-6'>
      <div className='mb-6'>
        <h2 className='text-2xl font-bold text-gray-900 mb-2'>
          DeepSeek AI Панель
        </h2>
        {providerInfo && (
          <div className='flex items-center gap-4 text-sm'>
            <span className='text-gray-600'>
              Провайдер: <strong>{providerInfo.provider}</strong>
            </span>
            <span
              className={`px-2 py-1 rounded-full text-xs ${
                providerInfo.configured
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {providerInfo.configured ? 'Настроен' : 'Не настроен'}
            </span>
          </div>
        )}
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

      {/* Settings Tab */}
      {activeTab === 'settings' && (
        <div className='space-y-4'>
          <APIKeyManager
            onSettingsChange={setApiSettings}
            initialSettings={apiSettings}
          />

          {/* Status Information */}
          <div className='bg-gray-50 p-4 rounded-md'>
            <h4 className='text-sm font-medium text-gray-900 mb-2'>
              Текущий статус
            </h4>
            <div className='text-xs text-gray-600 space-y-1'>
              <div>
                Режим:{' '}
                {apiSettings.useDirectClient
                  ? '🚀 Прямое подключение к Hugging Face'
                  : '🔄 Через backend сервер'}
              </div>
              <div>
                API ключ:{' '}
                {apiSettings.huggingfaceKey ? '✅ Настроен' : '❌ Не настроен'}
              </div>
              <div>
                Готовность:{' '}
                {(apiSettings.useDirectClient && apiSettings.huggingfaceKey) ||
                !apiSettings.useDirectClient
                  ? '✅ Готов к работе'
                  : '⚠️ Требует настройки API ключа'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Chat Tab */}
      {activeTab === 'chat' && (
        <div className='space-y-4'>
          {/* Quick Actions */}
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Быстрые действия
            </label>
            <div className='grid grid-cols-2 gap-2'>
              <button
                onClick={() => handleQuickAction('generate_landing')}
                disabled={loading}
                className='bg-green-600 text-white px-3 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 text-sm'
              >
                Создать лендинг
              </button>
              <button
                onClick={() => handleQuickAction('improve_seo')}
                disabled={loading}
                className='bg-purple-600 text-white px-3 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 text-sm'
              >
                Улучшить SEO
              </button>
              <button
                onClick={() => handleQuickAction('analyze_performance')}
                disabled={loading}
                className='bg-orange-600 text-white px-3 py-2 rounded-md hover:bg-orange-700 disabled:opacity-50 text-sm'
              >
                Анализ производительности
              </button>
              <button
                onClick={() => handleQuickAction('make_responsive')}
                disabled={loading}
                className='bg-indigo-600 text-white px-3 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50 text-sm'
              >
                Адаптивный дизайн
              </button>
            </div>
          </div>

          {/* Chat Messages */}
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Разговор с DeepSeek R1
            </label>
            <div className='border border-gray-300 rounded-md h-64 overflow-y-auto p-3 bg-gray-50'>
              {chatMessages.length === 0 ? (
                <div className='text-gray-500 text-center py-8'>
                  <p>Начните разговор с AI помощником</p>
                  <p className='text-sm mt-1'>
                    Попробуйте: "Создай лендинг для кафе" или "Улучши этот код"
                  </p>
                </div>
              ) : (
                <div className='space-y-3'>
                  {chatMessages.map((message, index) => (
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
                        <p className='text-sm'>{message.content}</p>
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
                          <div className='w-2 h-2 bg-gray-400 rounded-full animate-bounce'></div>
                          <div
                            className='w-2 h-2 bg-gray-400 rounded-full animate-bounce'
                            style={{ animationDelay: '0.1s' }}
                          ></div>
                          <div
                            className='w-2 h-2 bg-gray-400 rounded-full animate-bounce'
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
              placeholder='Опишите, что хотите создать или улучшить...'
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

          {/* AI Capabilities */}
          <div className='bg-blue-50 p-3 rounded-md'>
            <h4 className='text-sm font-medium text-blue-900 mb-2'>
              Возможности DeepSeek R1:
            </h4>
            <ul className='text-xs text-blue-800 space-y-1'>
              <li>• Создание HTML, CSS и JavaScript кода</li>
              <li>• Современный UI/UX дизайн</li>
              <li>• SEO оптимизация и мета-теги</li>
              <li>• Анализ кода и рекомендации</li>
              <li>• Адаптивный дизайн для всех устройств</li>
            </ul>
          </div>
        </div>
      )}

      {/* Content Enhancement Tab */}
      {activeTab === 'enhance' && (
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Тип улучшения
            </label>
            <select
              value={enhancementType}
              onChange={e => setEnhancementType(e.target.value)}
              className='w-full border border-gray-300 rounded-md px-3 py-2'
            >
              {enhancementTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Исходный контент
            </label>
            <textarea
              value={content}
              onChange={e => setContent(e.target.value)}
              rows={6}
              className='w-full border border-gray-300 rounded-md px-3 py-2'
              placeholder='Введите контент для улучшения...'
            />
          </div>
          <button
            onClick={handleEnhanceContent}
            disabled={loading || !content.trim()}
            className='bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50'
          >
            {loading ? 'Улучшение...' : 'Улучшить контент'}
          </button>
          {enhancedContent && (
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Улучшенный контент
              </label>
              <textarea
                value={enhancedContent}
                readOnly
                rows={6}
                className='w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50'
              />
            </div>
          )}
        </div>
      )}

      {/* HTML Generation Tab */}
      {activeTab === 'generate' && (
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Тип контента
            </label>
            <select
              value={contentType}
              onChange={e => setContentType(e.target.value)}
              className='w-full border border-gray-300 rounded-md px-3 py-2'
            >
              {contentTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Описание для генерации
            </label>
            <textarea
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              rows={4}
              className='w-full border border-gray-300 rounded-md px-3 py-2'
              placeholder='Опишите, какой HTML контент вы хотите сгенерировать...'
            />
          </div>
          <button
            onClick={handleGenerateHTML}
            disabled={loading || !prompt.trim()}
            className='bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50'
          >
            {loading ? 'Генерация...' : 'Сгенерировать HTML'}
          </button>
          {generatedHTML && (
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Сгенерированный HTML
              </label>
              <textarea
                value={generatedHTML}
                readOnly
                rows={8}
                className='w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 font-mono text-sm'
              />
            </div>
          )}
        </div>
      )}

      {/* Meta Tags Tab */}
      {activeTab === 'meta' && (
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Контент для анализа
            </label>
            <textarea
              value={metaContent}
              onChange={e => setMetaContent(e.target.value)}
              rows={6}
              className='w-full border border-gray-300 rounded-md px-3 py-2'
              placeholder='Введите контент для генерации мета-тегов...'
            />
          </div>
          <button
            onClick={handleGenerateMetaTags}
            disabled={loading || !metaContent.trim()}
            className='bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50'
          >
            {loading ? 'Генерация...' : 'Сгенерировать мета-теги'}
          </button>
          {metaTags.title && (
            <div className='space-y-3'>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-1'>
                  Заголовок
                </label>
                <input
                  type='text'
                  value={metaTags.title}
                  readOnly
                  className='w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50'
                />
              </div>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-1'>
                  Описание
                </label>
                <input
                  type='text'
                  value={metaTags.description}
                  readOnly
                  className='w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50'
                />
              </div>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-1'>
                  Ключевые слова
                </label>
                <input
                  type='text'
                  value={metaTags.keywords}
                  readOnly
                  className='w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50'
                />
              </div>
            </div>
          )}
        </div>
      )}

      {/* HTML Analysis Tab */}
      {activeTab === 'analyze' && (
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              HTML для анализа
            </label>
            <textarea
              value={htmlForAnalysis}
              onChange={e => setHtmlForAnalysis(e.target.value)}
              rows={6}
              className='w-full border border-gray-300 rounded-md px-3 py-2 font-mono text-sm'
              placeholder='Вставьте HTML код для анализа...'
            />
          </div>
          <button
            onClick={handleAnalyzeHTML}
            disabled={loading || !htmlForAnalysis.trim()}
            className='bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 disabled:opacity-50'
          >
            {loading ? 'Анализ...' : 'Анализировать HTML'}
          </button>
          {suggestions.length > 0 && (
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Рекомендации по улучшению
              </label>
              <ul className='space-y-2'>
                {suggestions.map((suggestion, index) => (
                  <li
                    key={index}
                    className='p-3 bg-yellow-50 border border-yellow-200 rounded-md text-sm'
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
