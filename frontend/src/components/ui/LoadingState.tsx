'use client';

import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { Code, Loader2, Sparkles, Zap } from 'lucide-react';

interface LoadingStateProps {
  isLoading: boolean;
  message?: string;
  progress?: number;
  className?: string;
  variant?: 'spinner' | 'dots' | 'pulse' | 'progress';
}

export default function LoadingState({
  isLoading,
  message = 'Генерируем...',
  progress,
  className,
  variant = 'spinner',
}: LoadingStateProps) {
  if (!isLoading) return null;

  const renderSpinner = () => (
    <div className='flex items-center space-x-3'>
      <Loader2 className='w-5 h-5 animate-spin text-blue-400' />
      <span className='text-gray-300'>{message}</span>
    </div>
  );

  const renderDots = () => (
    <div className='flex items-center space-x-3'>
      <div className='flex space-x-1'>
        <div className='w-2 h-2 bg-blue-400 rounded-full animate-bounce' />
        <div className='w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-100' />
        <div className='w-2 h-2 bg-pink-400 rounded-full animate-bounce delay-200' />
      </div>
      <span className='text-gray-300'>{message}</span>
    </div>
  );

  const renderPulse = () => (
    <div className='flex items-center space-x-3'>
      <div className='relative'>
        <div className='w-4 h-4 bg-blue-500 rounded-full animate-ping absolute' />
        <div className='w-4 h-4 bg-blue-400 rounded-full' />
      </div>
      <span className='text-gray-300'>{message}</span>
    </div>
  );

  const renderProgress = () => (
    <div className='w-full space-y-2'>
      <div className='flex justify-between items-center'>
        <span className='text-gray-300 text-sm'>{message}</span>
        {progress !== undefined && (
          <span className='text-gray-400 text-xs'>{Math.round(progress)}%</span>
        )}
      </div>
      <div className='w-full bg-gray-700 rounded-full h-2'>
        <motion.div
          className='bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full'
          initial={{ width: 0 }}
          animate={{
            width: progress !== undefined ? `${progress}%` : '60%',
          }}
          transition={{
            duration: progress !== undefined ? 0.3 : 2,
            repeat: progress === undefined ? Infinity : 0,
            repeatType: progress === undefined ? 'reverse' : undefined,
          }}
        />
      </div>
    </div>
  );

  const getContent = () => {
    switch (variant) {
      case 'dots':
        return renderDots();
      case 'pulse':
        return renderPulse();
      case 'progress':
        return renderProgress();
      default:
        return renderSpinner();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={cn(
        'flex items-center justify-center p-4 bg-gray-800/50 border border-gray-700 rounded-lg backdrop-blur-sm',
        className
      )}
    >
      {getContent()}
    </motion.div>
  );
}

// Компонент для полноэкранной загрузки
export function FullScreenLoading({
  message = 'Инициализация ИИ...',
  subMessage,
}: {
  message?: string;
  subMessage?: string;
}) {
  return (
    <div className='fixed inset-0 bg-[#0D1117] bg-opacity-95 backdrop-blur-sm flex items-center justify-center z-50'>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className='text-center space-y-6 max-w-md mx-auto p-8'
      >
        {/* Анимированная иконка */}
        <motion.div
          animate={{
            rotate: 360,
            scale: [1, 1.1, 1],
          }}
          transition={{
            rotate: { duration: 3, repeat: Infinity, ease: 'linear' },
            scale: { duration: 2, repeat: Infinity },
          }}
          className='w-16 h-16 mx-auto bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center'
        >
          <Sparkles className='w-8 h-8 text-white' />
        </motion.div>

        {/* Основное сообщение */}
        <div className='space-y-2'>
          <h3 className='text-xl font-semibold text-white'>{message}</h3>
          {subMessage && <p className='text-gray-400 text-sm'>{subMessage}</p>}
        </div>

        {/* Анимированные точки */}
        <div className='flex justify-center space-x-2'>
          <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
            className='w-3 h-3 bg-blue-400 rounded-full'
          />
          <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
            className='w-3 h-3 bg-purple-400 rounded-full'
          />
          <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
            className='w-3 h-3 bg-pink-400 rounded-full'
          />
        </div>

        {/* Прогресс бар */}
        <div className='w-full max-w-xs mx-auto'>
          <div className='h-1 bg-gray-700 rounded-full overflow-hidden'>
            <motion.div
              className='h-full bg-gradient-to-r from-blue-500 to-purple-500'
              animate={{
                x: ['-100%', '100%'],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
          </div>
        </div>
      </motion.div>
    </div>
  );
}

// Компонент с анимированными статусами для генерации
export function GenerationStatus({
  stage,
  progress,
}: {
  stage: 'analyzing' | 'generating' | 'optimizing' | 'finalizing';
  progress?: number;
}) {
  const stages = {
    analyzing: {
      icon: Zap,
      label: 'Анализируем требования',
      color: 'text-yellow-400',
    },
    generating: {
      icon: Code,
      label: 'Генерируем HTML код',
      color: 'text-blue-400',
    },
    optimizing: {
      icon: Sparkles,
      label: 'Оптимизируем результат',
      color: 'text-purple-400',
    },
    finalizing: {
      icon: Sparkles,
      label: 'Финализируем страницу',
      color: 'text-green-400',
    },
  };

  const currentStage = stages[stage];
  const Icon = currentStage.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className='flex items-center space-x-3 p-4 bg-gray-800/50 border border-gray-700 rounded-lg'
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
      >
        <Icon className={cn('w-5 h-5', currentStage.color)} />
      </motion.div>

      <div className='flex-1'>
        <p className='text-gray-300 text-sm'>{currentStage.label}</p>
        {progress !== undefined && (
          <div className='mt-1 w-full bg-gray-700 rounded-full h-1'>
            <motion.div
              className={cn('h-1 rounded-full bg-current', currentStage.color)}
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        )}
      </div>
    </motion.div>
  );
}
