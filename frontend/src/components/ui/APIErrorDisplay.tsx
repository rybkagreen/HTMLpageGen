'use client';

import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { AlertTriangle, ExternalLink, RefreshCw, Settings } from 'lucide-react';

interface APIErrorDisplayProps {
  error: string;
  onRetry?: () => void;
  className?: string;
}

export default function APIErrorDisplay({
  error,
  onRetry,
  className,
}: APIErrorDisplayProps) {
  const getErrorInfo = (error: string) => {
    if (error.includes('API key') || error.includes('Incorrect API key')) {
      return {
        title: 'Проблема с API ключом',
        description: 'DeepSeek API ключ не настроен или неверный',
        solution:
          'Получите ключ на platform.deepseek.com и добавьте в .env.local',
        link: 'https://platform.deepseek.com/api-keys',
        color: 'red',
      };
    }

    if (error.includes('rate_limit') || error.includes('Rate limit')) {
      return {
        title: 'Превышен лимит запросов',
        description: 'Достигнут лимит 100 запросов в час',
        solution: 'Подождите час или получите платный план',
        link: 'https://platform.deepseek.com/usage',
        color: 'orange',
      };
    }

    if (error.includes('insufficient_quota') || error.includes('quota')) {
      return {
        title: 'Недостаточно квоты',
        description: 'Закончилась бесплатная квота DeepSeek',
        solution: 'Пополните баланс или дождитесь обновления лимитов',
        link: 'https://platform.deepseek.com/billing',
        color: 'orange',
      };
    }

    if (
      error.includes('500') ||
      error.includes('502') ||
      error.includes('503')
    ) {
      return {
        title: 'Ошибка сервера DeepSeek',
        description: 'Временные проблемы с API DeepSeek',
        solution: 'Попробуйте через несколько минут',
        link: 'https://status.deepseek.com',
        color: 'blue',
      };
    }

    return {
      title: 'Неизвестная ошибка',
      description: error,
      solution: 'Проверьте консоль браузера для подробностей',
      link: 'https://platform.deepseek.com/docs',
      color: 'gray',
    };
  };

  const errorInfo = getErrorInfo(error);

  const colorClasses = {
    red: 'border-red-500/50 bg-red-500/10 text-red-300',
    orange: 'border-orange-500/50 bg-orange-500/10 text-orange-300',
    blue: 'border-blue-500/50 bg-blue-500/10 text-blue-300',
    gray: 'border-gray-500/50 bg-gray-500/10 text-gray-300',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        'border rounded-lg p-4',
        colorClasses[errorInfo.color as keyof typeof colorClasses],
        className
      )}
    >
      <div className='flex items-start space-x-3'>
        <AlertTriangle className='w-5 h-5 mt-0.5 flex-shrink-0' />

        <div className='flex-1 min-w-0'>
          <h3 className='font-semibold mb-1'>{errorInfo.title}</h3>
          <p className='text-sm opacity-90 mb-3'>{errorInfo.description}</p>

          <div className='space-y-2'>
            <div className='flex items-center text-sm'>
              <Settings className='w-4 h-4 mr-1.5' />
              <span className='font-medium'>Решение:</span>
            </div>
            <p className='text-sm pl-5 opacity-90'>{errorInfo.solution}</p>
          </div>

          <div className='flex items-center justify-between mt-4 pt-3 border-t border-current/20'>
            <a
              href={errorInfo.link}
              target='_blank'
              rel='noopener noreferrer'
              className='inline-flex items-center text-sm hover:underline'
            >
              Подробнее
              <ExternalLink className='w-3 h-3 ml-1' />
            </a>

            {onRetry && (
              <button
                onClick={onRetry}
                className='inline-flex items-center px-3 py-1 text-sm bg-current/20 hover:bg-current/30 rounded transition-colors'
              >
                <RefreshCw className='w-3 h-3 mr-1.5' />
                Повторить
              </button>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
