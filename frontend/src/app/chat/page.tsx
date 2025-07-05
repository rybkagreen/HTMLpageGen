'use client';

import ChatInterface from '@/components/ai/ChatInterface';
import { motion } from 'framer-motion';

export default function ChatPage() {
  return (
    <div className='min-h-screen bg-[#0D1117] text-white'>
      <div className='container mx-auto p-6'>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className='mb-6'
        >
          <h1 className='text-3xl font-bold mb-2'>ИИ Ассистент</h1>
          <p className='text-gray-400'>
            Общайтесь с ИИ для создания веб-страниц и получения помощи в
            разработке
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className='h-[calc(100vh-200px)]'
        >
          <ChatInterface />
        </motion.div>
      </div>
    </div>
  );
}
