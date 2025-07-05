'use client';
import { motion } from 'framer-motion';
import {
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  FileText,
  Target,
  Zap,
} from 'lucide-react';
interface GeneratedPage {
  html: string;
  meta: {
    generation_time: number;
    template_used: string;
    ai_enhanced: boolean;
    seo_score: number;
    word_count: number;
    meta_tags: { title: string; description: string; keywords: string };
  };
  plugins_applied: string[];
  generation_time: number;
}
interface StatusBarProps {
  isGenerating: boolean;
  generatedPage: GeneratedPage | null;
  error: string | null;
}
export default function StatusBar({
  isGenerating,
  generatedPage,
  error,
}: StatusBarProps) {
  const getSEOColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };
  const getSEOLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    return 'Needs Work';
  };
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className='border-t border-gray-800 bg-[#161B22] px-6 py-2'
    >
      {' '}
      <div className='flex items-center justify-between'>
        {' '}
        {/* Left Side - Status */}{' '}
        <div className='flex items-center space-x-4 text-sm'>
          {' '}
          {isGenerating && (
            <div className='flex items-center space-x-2 text-blue-400'>
              {' '}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              >
                {' '}
                <Activity className='w-4 h-4' />{' '}
              </motion.div>{' '}
              <span>Generating...</span>{' '}
            </div>
          )}{' '}
          {error && (
            <div className='flex items-center space-x-2 text-red-400'>
              {' '}
              <AlertCircle className='w-4 h-4' /> <span>{error}</span>{' '}
            </div>
          )}{' '}
          {!isGenerating && !error && generatedPage && (
            <div className='flex items-center space-x-2 text-green-400'>
              {' '}
              <CheckCircle className='w-4 h-4' />{' '}
              <span>Generation Complete</span>{' '}
            </div>
          )}{' '}
          {!isGenerating && !error && !generatedPage && (
            <div className='flex items-center space-x-2 text-gray-400'>
              {' '}
              <Zap className='w-4 h-4' /> <span>Ready to Generate</span>{' '}
            </div>
          )}{' '}
        </div>{' '}
        {/* Right Side - Stats */}{' '}
        {generatedPage && (
          <div className='flex items-center space-x-6 text-sm text-gray-400'>
            {' '}
            {/* Generation Time */}{' '}
            <div className='flex items-center space-x-1'>
              {' '}
              <Clock className='w-4 h-4' />{' '}
              <span>
                {(generatedPage.generation_time * 1000).toFixed(0)}ms
              </span>{' '}
            </div>{' '}
            {/* Word Count */}{' '}
            <div className='flex items-center space-x-1'>
              {' '}
              <FileText className='w-4 h-4' />{' '}
              <span>{generatedPage.meta.word_count} words</span>{' '}
            </div>{' '}
            {/* SEO Score */}{' '}
            <div className='flex items-center space-x-1'>
              {' '}
              <Target className='w-4 h-4' /> <span>SEO:</span>{' '}
              <span className={getSEOColor(generatedPage.meta.seo_score)}>
                {' '}
                {generatedPage.meta.seo_score}/100{' '}
              </span>{' '}
              <span
                className={`text-xs ${getSEOColor(generatedPage.meta.seo_score)}`}
              >
                {' '}
                ({getSEOLabel(generatedPage.meta.seo_score)}){' '}
              </span>{' '}
            </div>{' '}
            {/* Template */}{' '}
            <div className='flex items-center space-x-1'>
              {' '}
              <span>Template:</span>{' '}
              <span className='text-white capitalize'>
                {' '}
                {generatedPage.meta.template_used}{' '}
              </span>{' '}
            </div>{' '}
            {/* AI Enhanced */}{' '}
            {generatedPage.meta.ai_enhanced && (
              <div className='flex items-center space-x-1 text-purple-400'>
                {' '}
                <Zap className='w-4 h-4' /> <span>AI Enhanced</span>{' '}
              </div>
            )}{' '}
          </div>
        )}{' '}
      </div>
      {/* Progress Bar for Generation */}
      {isGenerating && (
        <div className='mt-2'>
          <div className='w-full bg-gray-700 rounded-full h-1'>
            <motion.div
              className='bg-blue-500 h-1 rounded-full'
              initial={{ width: '0%' }}
              animate={{ width: '100%' }}
              transition={{ duration: 2, ease: 'easeInOut' }}
            />
          </div>
        </div>
      )}
    </motion.div>
  );
}
