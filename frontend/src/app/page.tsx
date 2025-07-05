'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null; // Prevent hydration mismatch
  }

  return (
    <div className='min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900'>
      {/* Hero Section */}
      <div className='relative overflow-hidden'>
        <div className='absolute inset-0 bg-grid-white/10 bg-grid' />
        <div className='relative container mx-auto px-4 py-20 lg:py-32'>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className='text-center max-w-4xl mx-auto'
          >
            <div className='inline-flex items-center bg-blue-600/10 border border-blue-600/20 rounded-full px-4 py-2 mb-8'>
              <span className='w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse'></span>
              <span className='text-blue-400 text-sm font-medium'>
                AI-powered HTML Generation
              </span>
            </div>

            <h1 className='text-5xl lg:text-7xl font-bold tracking-tight text-white mb-6'>
              Создавайте{' '}
              <span className='bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent'>
                веб-страницы
              </span>{' '}
              с помощью ИИ
            </h1>

            <p className='text-xl text-gray-300 mb-10 leading-relaxed'>
              Превратите свои идеи в профессиональные HTML-страницы за секунды.
              Просто опишите что хотите — наш ИИ создаст идеальный код.
            </p>

            <div className='flex flex-col sm:flex-row gap-4 justify-center items-center'>
              <Link
                href='/generator'
                className='group relative inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-blue-600 rounded-xl hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1'
              >
                <span className='mr-2'>🚀</span>
                Начать создание
                <svg
                  className='ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform'
                  fill='none'
                  viewBox='0 0 24 24'
                  stroke='currentColor'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth={2}
                    d='M17 8l4 4m0 0l-4 4m4-4H3'
                  />
                </svg>
              </Link>

              <Link
                href='/docs'
                className='inline-flex items-center px-8 py-4 text-lg font-semibold text-gray-300 border border-gray-600 rounded-xl hover:bg-gray-800 hover:text-white transition-all duration-200'
              >
                Документация
              </Link>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Features Section */}
      <div className='py-20 bg-gray-800/50'>
        <div className='container mx-auto px-4'>
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className='text-center mb-16'
          >
            <h2 className='text-4xl font-bold text-white mb-4'>
              Почему выбирают нас?
            </h2>
            <p className='text-xl text-gray-400 max-w-2xl mx-auto'>
              Современные технологии и AI делают создание веб-страниц простым и
              быстрым
            </p>
          </motion.div>

          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'>
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className='group relative p-8 bg-gray-900/50 border border-gray-700 rounded-2xl hover:border-blue-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/10'
              >
                <div className='inline-flex items-center justify-center w-12 h-12 bg-blue-600/10 border border-blue-600/20 rounded-lg mb-6 group-hover:bg-blue-600/20 transition-colors'>
                  <span className='text-2xl'>{feature.icon}</span>
                </div>

                <h3 className='text-xl font-semibold text-white mb-3 group-hover:text-blue-400 transition-colors'>
                  {feature.title}
                </h3>

                <p className='text-gray-400 leading-relaxed'>
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className='py-20 bg-gradient-to-r from-blue-900/20 to-purple-900/20'>
        <div className='container mx-auto px-4'>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-8 text-center'>
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className='p-8'
              >
                <div className='text-4xl lg:text-5xl font-bold text-white mb-2'>
                  {stat.value}
                </div>
                <div className='text-gray-400 text-lg'>{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className='py-20'>
        <div className='container mx-auto px-4 text-center'>
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className='max-w-3xl mx-auto'
          >
            <h2 className='text-4xl font-bold text-white mb-6'>
              Готовы создать что-то удивительное?
            </h2>
            <p className='text-xl text-gray-400 mb-10'>
              Присоединяйтесь к тысячам разработчиков, которые уже используют
              наш AI для создания веб-страниц
            </p>
            <Link
              href='/generator'
              className='inline-flex items-center px-10 py-5 text-xl font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-2xl hover:shadow-blue-500/25 transform hover:-translate-y-1'
            >
              Начать бесплатно
              <svg
                className='ml-3 w-6 h-6'
                fill='none'
                viewBox='0 0 24 24'
                stroke='currentColor'
              >
                <path
                  strokeLinecap='round'
                  strokeLinejoin='round'
                  strokeWidth={2}
                  d='M13 7l5 5m0 0l-5 5m5-5H6'
                />
              </svg>
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

const features = [
  {
    icon: '🤖',
    title: 'AI-powered генерация',
    description:
      'Искусственный интеллект создает уникальный HTML-код на основе вашего описания, экономя часы работы.',
  },
  {
    icon: '⚡',
    title: 'Молниеносная скорость',
    description:
      'Получите готовую веб-страницу за секунды. Никакого ожидания, только мгновенные результаты.',
  },
  {
    icon: '🎨',
    title: 'Современный дизайн',
    description:
      'Все страницы создаются с учетом современных трендов дизайна и лучших практик UX/UI.',
  },
  {
    icon: '📱',
    title: 'Адаптивность',
    description:
      'Все генерируемые страницы автоматически адаптируются под любые устройства и экраны.',
  },
  {
    icon: '🔍',
    title: 'SEO-оптимизация',
    description:
      'Встроенная SEO-оптимизация обеспечивает лучшее ранжирование в поисковых системах.',
  },
  {
    icon: '⚙️',
    title: 'Гибкая настройка',
    description:
      'Множество шаблонов и возможностей кастомизации для создания уникального дизайна.',
  },
];

const stats = [
  { value: '10K+', label: 'Созданных страниц' },
  { value: '99.9%', label: 'Время работы' },
  { value: '< 2s', label: 'Время генерации' },
];
