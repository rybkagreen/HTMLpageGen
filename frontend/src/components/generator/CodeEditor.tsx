'use client';

import { motion } from 'framer-motion';
import { Check, Copy, Download, FileText } from 'lucide-react';
import { useState } from 'react';

interface CodeEditorProps {
  code: string;
  onChange?: (value: string) => void;
  language?: string;
  readOnly?: boolean;
  height?: string;
}

export default function CodeEditor({
  code,
  onChange,
  language = 'html',
  readOnly = false,
  height = '100%',
}: CodeEditorProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'generated-page.html';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className='flex flex-col h-full bg-[#0D1117]'>
      {/* Editor Header */}
      <div className='flex items-center justify-between px-4 py-2 bg-[#161B22] border-b border-gray-800'>
        <div className='flex items-center space-x-2 text-sm text-gray-400'>
          <FileText className='w-4 h-4' />
          <span className='capitalize'>{language}</span>
          {code && <span>• {code.split('\n').length} lines</span>}
        </div>

        <div className='flex items-center space-x-1'>
          <button
            onClick={handleCopy}
            disabled={!code}
            className='p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed'
            title='Copy to Clipboard'
          >
            {copied ? (
              <motion.div
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className='text-green-400'
              >
                <Check className='w-4 h-4' />
              </motion.div>
            ) : (
              <Copy className='w-4 h-4' />
            )}
          </button>

          <button
            onClick={handleDownload}
            disabled={!code}
            className='p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed'
            title='Download HTML'
          >
            <Download className='w-4 h-4' />
          </button>
        </div>
      </div>

      {/* Code Display */}
      <div className='flex-1 relative overflow-auto'>
        {code ? (
          <pre className='h-full p-4 text-sm text-gray-300 font-mono leading-relaxed whitespace-pre-wrap'>
            <code>{code}</code>
          </pre>
        ) : (
          <div className='absolute inset-0 flex items-center justify-center bg-[#0D1117] text-gray-500'>
            <div className='text-center'>
              <FileText className='w-8 h-8 mx-auto mb-2 opacity-50' />
              <p>Ваш сгенерированный HTML появится здесь</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
