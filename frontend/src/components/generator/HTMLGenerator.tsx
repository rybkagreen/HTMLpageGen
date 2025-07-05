'use client';

import { AIAgent, RequirementAnalysis } from '@/lib/ai-agent';
import { Project, ProjectManager } from '@/lib/project-manager';
import { cn } from '@/lib/utils';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Code,
  Download,
  Eye,
  FileText,
  Monitor,
  Play,
  RotateCcw,
  Settings,
  Smartphone,
  Sparkles,
  Tablet,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { handleApiError, useErrorHandler } from '../ui/ErrorHandler';
import CodeEditor from './CodeEditor';
import PreviewPanel from './PreviewPanel';
import SettingsPanel from './SettingsPanel';
import StatusBar from './StatusBar';

interface GenerateRequest {
  title: string;
  content: string;
  template: 'basic' | 'modern' | 'minimal' | 'business' | 'blog';
  style?: 'light' | 'dark' | 'blue' | 'purple';
  features?: string[];
  ai_enhance?: boolean;
}

interface GeneratedPage {
  html: string;
  meta: {
    generation_time: number;
    template_used: string;
    ai_enhanced: boolean;
    seo_score: number;
    word_count: number;
    meta_tags: {
      title: string;
      description: string;
      keywords: string;
    };
  };
  plugins_applied: string[];
  generation_time: number;
}

const TEMPLATES = [
  { id: 'basic', name: 'Basic', description: 'Простая и чистая страница' },
  {
    id: 'modern',
    name: 'Modern',
    description: 'Современный дизайн с градиентами',
  },
  { id: 'minimal', name: 'Minimal', description: 'Минималистичный стиль' },
  { id: 'business', name: 'Business', description: 'Корпоративный стиль' },
  { id: 'blog', name: 'Blog', description: 'Макет для блога' },
] as const;

const DEVICE_SIZES = [
  { id: 'desktop', name: 'Desktop', icon: Monitor, width: '100%' },
  { id: 'tablet', name: 'Tablet', icon: Tablet, width: '768px' },
  { id: 'mobile', name: 'Mobile', icon: Smartphone, width: '375px' },
] as const;

export default function HTMLGenerator() {
  const [generatedPage, setGeneratedPage] = useState<GeneratedPage | null>(
    null
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [showCode, setShowCode] = useState(true);
  const [previewDevice, setPreviewDevice] = useState<
    'desktop' | 'tablet' | 'mobile'
  >('desktop');
  const [showSettings, setShowSettings] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [livePreview, setLivePreview] = useState(true);
  const [analysis, setAnalysis] = useState<RequirementAnalysis | null>(null);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);

  // Обработка ошибок
  const { showError, showSuccess, ErrorComponent } = useErrorHandler();

  const [aiAgent] = useState(
    () =>
      new AIAgent({
        messages: [],
        userPreferences: {
          preferredFrameworks: ['html', 'css'],
          designStyle: 'modern',
          complexity: 'medium',
        },
        sessionGoals: [],
      })
  );
  const [projectManager] = useState(() => new ProjectManager());

  const [formData, setFormData] = useState<GenerateRequest>({
    title: '',
    content: '',
    template: 'modern',
    style: 'dark',
    features: [],
    ai_enhance: true,
  });

  // Анализ требований при изменении контента
  useEffect(() => {
    const analyzeContent = async () => {
      if (formData.title && formData.content) {
        try {
          const userInput = `${formData.title}. ${formData.content}`;
          const analysisResult = await aiAgent.analyzeRequirements(userInput);
          setAnalysis(analysisResult);

          // Автоматически обновляем шаблон если анализ предлагает другой
          if (analysisResult.suggestedTemplate !== formData.template) {
            setFormData(prev => ({
              ...prev,
              template: analysisResult.suggestedTemplate as any,
            }));
          }
        } catch (error) {
          console.error('Analysis error:', error);
        }
      } else {
        setAnalysis(null);
      }
    };

    const timeoutId = setTimeout(analyzeContent, 1000); // Дебаунс
    return () => clearTimeout(timeoutId);
  }, [formData.title, formData.content, aiAgent]);

  const handleGenerate = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      showError({
        title: 'Не заполнены поля',
        message: 'Пожалуйста, заполните название и содержимое страницы',
      });
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch {
          // Если не удается прочитать JSON, используем статус код
        }
        throw new Error(errorMessage);
      }

      const result: GeneratedPage = await response.json();
      setGeneratedPage(result);

      // Показываем успешное сообщение
      showSuccess({
        title: 'Страница создана!',
        message: `HTML-страница "${formData.title}" успешно сгенерирована за ${result.generation_time.toFixed(1)}с`,
      });

      // Автоматически сохраняем проект
      if (result.html) {
        await saveProject(result.html);
      }

      if (!showPreview) {
        setShowPreview(true);
      }
    } catch (err: any) {
      console.error('Generation failed:', err);
      handleApiError(err, showError);
      setError('Ошибка при генерации страницы. Попробуйте снова.');
    } finally {
      setIsGenerating(false);
    }
  };

  const saveProject = async (html: string) => {
    try {
      if (currentProject) {
        // Обновляем существующий проект
        currentProject.files[0].content = html;
        currentProject.files[0].lastModified = new Date();
        currentProject.updatedAt = new Date();
        await projectManager.saveProject(currentProject);
      } else {
        // Создаем новый проект
        const project = await projectManager.createProject({
          name: formData.title || 'Новый проект',
          type: 'website',
          html,
          prompt: `${formData.title}. ${formData.content}`,
          metadata: {
            description: formData.content.substring(0, 160),
            tags: formData.features || [],
            technologies: ['html', 'css'],
            difficulty:
              analysis?.complexity === 'simple'
                ? 'beginner'
                : analysis?.complexity === 'complex'
                  ? 'advanced'
                  : 'intermediate',
            estimatedTime: analysis?.estimatedTime || 30,
          },
        });
        setCurrentProject(project);
      }
    } catch (error) {
      console.error('Error saving project:', error);
    }
  };

  const handleDownload = () => {
    if (!generatedPage) return;

    const blob = new Blob([generatedPage.html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${formData.title.toLowerCase().replace(/\s+/g, '-')}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleReset = () => {
    setGeneratedPage(null);
    setFormData({
      title: '',
      content: '',
      template: 'modern',
      style: 'dark',
      features: [],
      ai_enhance: true,
    });
    setError(null);
  };

  const currentDeviceSize = DEVICE_SIZES.find(d => d.id === previewDevice);

  return (
    <div className='min-h-screen bg-[#0D1117] text-white flex flex-col'>
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className='border-b border-gray-800 bg-[#161B22] px-6 py-4'
      >
        <div className='flex items-center justify-between'>
          <div className='flex items-center space-x-4'>
            <div className='flex items-center space-x-2'>
              <div className='w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center'>
                <Sparkles className='w-4 h-4 text-white' />
              </div>
              <h1 className='text-xl font-bold'>HTML Generator</h1>
            </div>
          </div>

          <div className='flex items-center space-x-2'>
            {/* View Controls */}
            <div className='flex items-center bg-gray-800 rounded-lg p-1'>
              <button
                onClick={() => setShowCode(!showCode)}
                className={cn(
                  'px-3 py-1.5 rounded text-sm font-medium transition-colors',
                  showCode
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700'
                )}
              >
                <Code className='w-4 h-4 mr-1.5 inline' />
                Code
              </button>
              <button
                onClick={() => setShowPreview(!showPreview)}
                className={cn(
                  'px-3 py-1.5 rounded text-sm font-medium transition-colors',
                  showPreview
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700'
                )}
              >
                <Eye className='w-4 h-4 mr-1.5 inline' />
                Preview
              </button>
            </div>

            {/* Device Size Controls */}
            {showPreview && (
              <div className='flex items-center bg-gray-800 rounded-lg p-1'>
                {DEVICE_SIZES.map(device => {
                  const Icon = device.icon;
                  return (
                    <button
                      key={device.id}
                      onClick={() => setPreviewDevice(device.id as any)}
                      className={cn(
                        'p-2 rounded transition-colors',
                        previewDevice === device.id
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-400 hover:text-white hover:bg-gray-700'
                      )}
                      title={device.name}
                    >
                      <Icon className='w-4 h-4' />
                    </button>
                  );
                })}
              </div>
            )}

            {/* Action Buttons */}
            <div className='flex items-center space-x-1'>
              <button
                onClick={() => setShowSettings(true)}
                className='p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors'
                title='Settings'
              >
                <Settings className='w-4 h-4' />
              </button>

              {generatedPage && (
                <>
                  <button
                    onClick={handleDownload}
                    className='p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors'
                    title='Download'
                  >
                    <Download className='w-4 h-4' />
                  </button>
                </>
              )}

              <button
                onClick={handleReset}
                className='p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors'
                title='Reset'
              >
                <RotateCcw className='w-4 h-4' />
              </button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className='flex-1 flex overflow-hidden'>
        {/* Input Panel */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className='w-80 border-r border-gray-800 bg-[#161B22] flex flex-col'
        >
          <div className='p-6 border-b border-gray-800'>
            <h2 className='text-lg font-semibold mb-4 flex items-center'>
              <FileText className='w-5 h-5 mr-2' />
              Content
            </h2>

            <div className='space-y-4'>
              <div>
                <label className='block text-sm font-medium text-gray-300 mb-2'>
                  Название страницы
                </label>
                <input
                  type='text'
                  value={formData.title}
                  onChange={e =>
                    setFormData(prev => ({ ...prev, title: e.target.value }))
                  }
                  placeholder='Введите название...'
                  className='w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none'
                />
              </div>

              <div>
                <label className='block text-sm font-medium text-gray-300 mb-2'>
                  Содержимое
                </label>
                <textarea
                  value={formData.content}
                  onChange={e =>
                    setFormData(prev => ({ ...prev, content: e.target.value }))
                  }
                  placeholder='Опишите содержимое страницы...'
                  rows={6}
                  className='w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none resize-none'
                />
              </div>

              <div>
                <label className='block text-sm font-medium text-gray-300 mb-2'>
                  Шаблон
                </label>
                <select
                  value={formData.template}
                  onChange={e =>
                    setFormData(prev => ({
                      ...prev,
                      template: e.target.value as any,
                    }))
                  }
                  className='w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none'
                >
                  {TEMPLATES.map(template => (
                    <option key={template.id} value={template.id}>
                      {template.name} - {template.description}
                    </option>
                  ))}
                </select>
              </div>

              {/* AI Analysis Panel */}
              {analysis && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className='p-4 bg-blue-900/20 border border-blue-700/50 rounded-lg'
                >
                  <div className='flex items-center mb-2'>
                    <Sparkles className='w-4 h-4 mr-2 text-blue-400' />
                    <span className='text-sm font-medium text-blue-300'>
                      ИИ Анализ
                    </span>
                  </div>

                  <div className='text-sm space-y-2'>
                    <div className='flex items-center space-x-4'>
                      <span className='text-gray-400'>Намерение:</span>
                      <span className='text-blue-300'>{analysis.intent}</span>
                    </div>
                    <div className='flex items-center space-x-4'>
                      <span className='text-gray-400'>Сложность:</span>
                      <span className='text-blue-300'>
                        {analysis.complexity}
                      </span>
                    </div>
                    <div className='flex items-center space-x-4'>
                      <span className='text-gray-400'>Время:</span>
                      <span className='text-blue-300'>
                        ~{analysis.estimatedTime} мин
                      </span>
                    </div>

                    {analysis.recommendations.length > 0 && (
                      <div className='mt-2'>
                        <span className='text-gray-400 text-xs'>
                          Рекомендации:
                        </span>
                        <ul className='text-xs text-gray-300 mt-1 space-y-1'>
                          {analysis.recommendations
                            .slice(0, 3)
                            .map((rec, i) => (
                              <li key={i} className='flex items-start'>
                                <span className='text-blue-400 mr-1'>•</span>
                                {rec}
                              </li>
                            ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}

              {error && (
                <div className='p-3 bg-red-900/20 border border-red-500/30 rounded-lg'>
                  <p className='text-red-300 text-sm'>{error}</p>
                </div>
              )}

              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className='w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2'
              >
                {isGenerating ? (
                  <>
                    <div className='w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin' />
                    <span>Генерация...</span>
                  </>
                ) : (
                  <>
                    <Play className='w-4 h-4' />
                    <span>Сгенерировать</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </motion.div>

        {/* Code and Preview Panels */}
        <div className='flex-1 flex'>
          {/* Code Editor */}
          <AnimatePresence>
            {showCode && (
              <motion.div
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: showPreview ? '50%' : '100%' }}
                exit={{ opacity: 0, width: 0 }}
                transition={{ duration: 0.3 }}
                className='border-r border-gray-800'
              >
                <CodeEditor
                  code={generatedPage?.html || ''}
                  language='html'
                  readOnly={!generatedPage}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Preview Panel */}
          <AnimatePresence>
            {showPreview && (
              <motion.div
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: showCode ? '50%' : '100%' }}
                exit={{ opacity: 0, width: 0 }}
                transition={{ duration: 0.3 }}
                className='flex flex-col'
              >
                <PreviewPanel
                  html={generatedPage?.html}
                  deviceSize={currentDeviceSize?.width}
                  livePreview={livePreview}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Status Bar */}
      <StatusBar
        isGenerating={isGenerating}
        generatedPage={generatedPage}
        error={error}
      />

      {/* Settings Modal */}
      <SettingsPanel
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        formData={formData}
        onFormDataChange={setFormData}
        livePreview={livePreview}
        onLivePreviewChange={setLivePreview}
      />

      {/* Error Handler */}
      <ErrorComponent />
    </div>
  );
}
