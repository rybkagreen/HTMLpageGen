'use client';

import { cn } from '@/lib/utils';
import { AnimatePresence, motion } from 'framer-motion';
import {
  AlertTriangle,
  CheckCircle,
  ExternalLink,
  Info,
  RefreshCw,
  X,
  XCircle,
} from 'lucide-react';
import { useEffect, useState } from 'react';

export interface APIError {
  type: 'error' | 'warning' | 'info' | 'success';
  title: string;
  message: string;
  details?: string;
  code?: string;
  action?: {
    label: string;
    onClick: () => void;
    external?: boolean;
  };
  retryAction?: () => void;
  dismissible?: boolean;
  autoHide?: number; // Время в секундах
}

interface ErrorHandlerProps {
  error: APIError | null;
  onDismiss?: () => void;
  className?: string;
}

const ERROR_ICONS = {
  error: XCircle,
  warning: AlertTriangle,
  info: Info,
  success: CheckCircle,
};

const ERROR_STYLES = {
  error: {
    bg: 'bg-red-950/50 border-red-500/30',
    icon: 'text-red-400',
    text: 'text-red-100',
    title: 'text-red-200',
  },
  warning: {
    bg: 'bg-yellow-950/50 border-yellow-500/30',
    icon: 'text-yellow-400',
    text: 'text-yellow-100',
    title: 'text-yellow-200',
  },
  info: {
    bg: 'bg-blue-950/50 border-blue-500/30',
    icon: 'text-blue-400',
    text: 'text-blue-100',
    title: 'text-blue-200',
  },
  success: {
    bg: 'bg-green-950/50 border-green-500/30',
    icon: 'text-green-400',
    text: 'text-green-100',
    title: 'text-green-200',
  },
};

export default function ErrorHandler({
  error,
  onDismiss,
  className,
}: ErrorHandlerProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (error) {
      setIsVisible(true);

      // Автоскрытие
      if (error.autoHide) {
        const timer = setTimeout(() => {
          handleDismiss();
        }, error.autoHide * 1000);

        return () => clearTimeout(timer);
      }
    } else {
      setIsVisible(false);
    }
  }, [error]);

  const handleDismiss = () => {
    setIsVisible(false);
    setTimeout(() => {
      onDismiss?.();
    }, 300); // Время анимации
  };

  if (!error) return null;

  const Icon = ERROR_ICONS[error.type];
  const styles = ERROR_STYLES[error.type];

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.95 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
          className={cn('fixed top-4 right-4 z-50 max-w-md w-full', className)}
        >
          <div
            className={cn(
              'p-4 rounded-lg border backdrop-blur-sm shadow-xl',
              styles.bg
            )}
          >
            <div className='flex items-start space-x-3'>
              <Icon
                className={cn('w-5 h-5 mt-0.5 flex-shrink-0', styles.icon)}
              />

              <div className='flex-1 min-w-0'>
                <h4 className={cn('font-semibold text-sm', styles.title)}>
                  {error.title}
                </h4>

                <p className={cn('mt-1 text-sm', styles.text)}>
                  {error.message}
                </p>

                {error.details && (
                  <details className='mt-2'>
                    <summary
                      className={cn(
                        'cursor-pointer text-xs opacity-80 hover:opacity-100 transition-opacity',
                        styles.text
                      )}
                    >
                      Подробности
                    </summary>
                    <pre
                      className={cn(
                        'mt-2 text-xs p-2 bg-black/20 rounded border overflow-x-auto',
                        styles.text
                      )}
                    >
                      {error.details}
                    </pre>
                  </details>
                )}

                {error.code && (
                  <div className={cn('mt-2 text-xs opacity-70', styles.text)}>
                    Код ошибки: {error.code}
                  </div>
                )}

                {(error.action || error.retryAction) && (
                  <div className='flex items-center space-x-2 mt-3'>
                    {error.retryAction && (
                      <button
                        onClick={error.retryAction}
                        className={cn(
                          'inline-flex items-center px-3 py-1.5 text-xs font-medium rounded transition-colors',
                          error.type === 'error'
                            ? 'bg-red-600 hover:bg-red-700 text-white'
                            : error.type === 'warning'
                              ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                              : 'bg-blue-600 hover:bg-blue-700 text-white'
                        )}
                      >
                        <RefreshCw className='w-3 h-3 mr-1' />
                        Повторить
                      </button>
                    )}

                    {error.action && (
                      <button
                        onClick={error.action.onClick}
                        className={cn(
                          'inline-flex items-center px-3 py-1.5 text-xs font-medium rounded transition-colors',
                          'bg-gray-600 hover:bg-gray-700 text-white'
                        )}
                      >
                        {error.action.label}
                        {error.action.external && (
                          <ExternalLink className='w-3 h-3 ml-1' />
                        )}
                      </button>
                    )}
                  </div>
                )}
              </div>

              {error.dismissible !== false && (
                <button
                  onClick={handleDismiss}
                  className={cn(
                    'p-1 rounded transition-colors flex-shrink-0',
                    styles.text,
                    'hover:bg-white/10'
                  )}
                >
                  <X className='w-4 h-4' />
                </button>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// Хук для управления ошибками
export function useErrorHandler() {
  const [error, setError] = useState<APIError | null>(null);

  const showError = (
    errorConfig: Omit<APIError, 'type'> & { type?: APIError['type'] }
  ) => {
    setError({
      type: 'error',
      dismissible: true,
      ...errorConfig,
    });
  };

  const showWarning = (errorConfig: Omit<APIError, 'type'>) => {
    setError({
      type: 'warning',
      dismissible: true,
      autoHide: 5,
      ...errorConfig,
    });
  };

  const showInfo = (errorConfig: Omit<APIError, 'type'>) => {
    setError({
      type: 'info',
      dismissible: true,
      autoHide: 4,
      ...errorConfig,
    });
  };

  const showSuccess = (errorConfig: Omit<APIError, 'type'>) => {
    setError({
      type: 'success',
      dismissible: true,
      autoHide: 3,
      ...errorConfig,
    });
  };

  const clearError = () => {
    setError(null);
  };

  return {
    error,
    showError,
    showWarning,
    showInfo,
    showSuccess,
    clearError,
    ErrorComponent: () => <ErrorHandler error={error} onDismiss={clearError} />,
  };
}

// Утилита для обработки API ошибок
export function handleApiError(error: any, showError: (config: any) => void) {
  console.error('API Error:', error);

  if (error.message?.includes('insufficient_balance')) {
    showError({
      title: 'Недостаточно средств',
      message:
        'На балансе DeepSeek недостаточно средств для выполнения запроса.',
      details: error.message,
      action: {
        label: 'Пополнить баланс',
        onClick: () =>
          window.open('https://platform.deepseek.com/usage', '_blank'),
        external: true,
      },
    });
  } else if (error.message?.includes('rate_limit')) {
    showError({
      title: 'Превышен лимит запросов',
      message: 'Слишком много запросов за короткое время. Попробуйте позже.',
      details: error.message,
      retryAction: () => {
        // Повторный вызов будет реализован в компоненте
      },
    });
  } else if (error.message?.includes('unauthorized')) {
    showError({
      title: 'Ошибка авторизации',
      message: 'Неверный API ключ DeepSeek. Проверьте настройки.',
      details: error.message,
      action: {
        label: 'Получить ключ',
        onClick: () =>
          window.open('https://platform.deepseek.com/api_keys', '_blank'),
        external: true,
      },
    });
  } else if (error.message?.includes('network')) {
    showError({
      title: 'Проблема с сетью',
      message:
        'Не удается подключиться к серверу. Проверьте интернет-соединение.',
      details: error.message,
      retryAction: () => {
        // Повторный вызов будет реализован в компоненте
      },
    });
  } else {
    showError({
      title: 'Произошла ошибка',
      message: error.message || 'Неизвестная ошибка при выполнении запроса.',
      details: error.stack || JSON.stringify(error),
      code: error.code,
    });
  }
}
