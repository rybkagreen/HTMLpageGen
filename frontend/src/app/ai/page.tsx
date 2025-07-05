import DeepSeekAIPanel from '@/components/ai/DeepSeekAIPanel';
import Layout from '@/components/layout/Layout';

export default function AIPage() {
  return (
    <Layout>
      <div className='min-h-screen bg-gray-50 py-8'>
        <div className='max-w-6xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='mb-8'>
            <h1 className='text-3xl font-bold text-gray-900'>
              AI Возможности с DeepSeek
            </h1>
            <p className='mt-2 text-gray-600'>
              Используйте мощные возможности искусственного интеллекта DeepSeek
              R1 для улучшения контента, генерации HTML и SEO оптимизации.
            </p>
          </div>

          <div className='grid gap-8'>
            <DeepSeekAIPanel />

            <div className='bg-white rounded-lg shadow-lg p-6'>
              <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                Возможности DeepSeek R1
              </h3>
              <div className='grid md:grid-cols-2 gap-6'>
                <div>
                  <h4 className='font-medium text-gray-800 mb-2'>
                    📝 Улучшение контента
                  </h4>
                  <p className='text-sm text-gray-600'>
                    Автоматическое улучшение текста для веб-сайтов с учетом SEO,
                    доступности и маркетинговых задач.
                  </p>
                </div>
                <div>
                  <h4 className='font-medium text-gray-800 mb-2'>
                    🏗️ Генерация HTML
                  </h4>
                  <p className='text-sm text-gray-600'>
                    Создание семантически правильного HTML на основе текстового
                    описания.
                  </p>
                </div>
                <div>
                  <h4 className='font-medium text-gray-800 mb-2'>
                    🏷️ Мета-теги
                  </h4>
                  <p className='text-sm text-gray-600'>
                    Автоматическая генерация SEO-оптимизированных мета-тегов на
                    основе содержимого.
                  </p>
                </div>
                <div>
                  <h4 className='font-medium text-gray-800 mb-2'>
                    🔍 Анализ HTML
                  </h4>
                  <p className='text-sm text-gray-600'>
                    Получение рекомендаций по улучшению существующего HTML для
                    SEO и доступности.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
