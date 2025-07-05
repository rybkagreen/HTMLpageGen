'use client';
import { motion } from 'framer-motion';
import { AlertTriangle, ExternalLink, RefreshCw } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
interface PreviewPanelProps {
  html?: string;
  deviceSize?: string;
  livePreview?: boolean;
}
export default function PreviewPanel({
  html,
  deviceSize = '100%',
  livePreview = true,
}: PreviewPanelProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    if (html && iframeRef.current && livePreview) {
      updatePreview();
    }
  }, [html, livePreview]);
  const updatePreview = () => {
    if (!html || !iframeRef.current) return;
    setIsLoading(true);
    setError(null);
    try {
      const iframe = iframeRef.current;
      const doc = iframe.contentDocument || iframe.contentWindow?.document;
      if (doc) {
        doc.open();
        doc.write(html);
        doc.close();
        iframe.onload = () => {
          setIsLoading(false);
        };
        iframe.onerror = () => {
          setIsLoading(false);
          setError('Failed to load preview');
        };
      }
    } catch (err) {
      setIsLoading(false);
      setError('Failed to render preview');
      console.error('Preview error:', err);
    }
  };
  const handleRefresh = () => {
    updatePreview();
  };
  const handleOpenInNewTab = () => {
    if (!html) return;
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  return (
    <div className='flex flex-col h-full bg-[#0D1117]'>
      {' '}
      <div className='flex items-center justify-between px-4 py-2 bg-[#161B22] border-b border-gray-800'>
        {' '}
        <div className='flex items-center space-x-2'>
          {' '}
          {isLoading && (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            >
              {' '}
              <RefreshCw className='w-4 h-4 text-blue-400' />{' '}
            </motion.div>
          )}{' '}
          {error && (
            <div className='flex items-center space-x-1 text-red-400'>
              {' '}
              <AlertTriangle className='w-4 h-4' />{' '}
              <span className='text-sm'>{error}</span>{' '}
            </div>
          )}{' '}
          {!isLoading && !error && html && (
            <div className='flex items-center space-x-1 text-green-400'>
              {' '}
              <div className='w-2 h-2 bg-green-400 rounded-full'></div>{' '}
              <span className='text-sm'>Live</span>{' '}
            </div>
          )}{' '}
        </div>{' '}
        <div className='flex items-center space-x-1'>
          {' '}
          <button
            onClick={handleRefresh}
            disabled={!html}
            className='p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors disabled:opacity-50'
            title='Refresh Preview'
          >
            {' '}
            <RefreshCw className='w-4 h-4' />{' '}
          </button>{' '}
          <button
            onClick={handleOpenInNewTab}
            disabled={!html}
            className='p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors disabled:opacity-50'
            title='Open in New Tab'
          >
            {' '}
            <ExternalLink className='w-4 h-4' />{' '}
          </button>{' '}
        </div>{' '}
      </div>{' '}
      <div className='flex-1 flex items-center justify-center bg-gray-900 p-4'>
        {' '}
        {html ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2 }}
            className='w-full h-full flex justify-center'
            style={{ maxWidth: deviceSize === '100%' ? '100%' : deviceSize }}
          >
            {' '}
            <iframe
              ref={iframeRef}
              className='w-full h-full bg-white rounded-lg shadow-2xl border border-gray-700'
              sandbox='allow-scripts allow-same-origin allow-forms'
              title='HTML Preview'
            />{' '}
          </motion.div>
        ) : (
          <div className='text-center text-gray-500'>
            {' '}
            <div className='w-16 h-16 mx-auto mb-4 bg-gray-800 rounded-lg flex items-center justify-center'>
              {' '}
              <ExternalLink className='w-8 h-8 opacity-50' />{' '}
            </div>{' '}
            <p className='text-lg mb-2'>
              Нет содержимого для предварительного просмотра
            </p>{' '}
            <p className='text-sm'>
              Сгенерируйте HTML страницу, чтобы увидеть предварительный просмотр
            </p>{' '}
          </div>
        )}{' '}
      </div>{' '}
      {deviceSize !== '100%' && (
        <div className='px-4 py-2 bg-[#161B22] border-t border-gray-800 text-center'>
          {' '}
          <span className='text-xs text-gray-400'>
            Viewing at {deviceSize} width
          </span>
        </div>
      )}
    </div>
  );
}
