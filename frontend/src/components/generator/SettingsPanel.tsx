'use client';
import { AnimatePresence, motion } from 'framer-motion';
import { Palette, Settings, Shield, X, Zap } from 'lucide-react';
import { useState } from 'react';
interface GenerateRequest {
  title: string;
  content: string;
  template: 'basic' | 'modern' | 'minimal' | 'business' | 'blog';
  style?: 'light' | 'dark' | 'blue' | 'purple';
  features?: string[];
  ai_enhancements?: boolean;
}
interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  formData: GenerateRequest;
  onFormDataChange: (data: GenerateRequest) => void;
  livePreview: boolean;
  onLivePreviewChange: (enabled: boolean) => void;
}
const STYLES = [
  { id: 'light', name: 'Light', color: '#ffffff' },
  { id: 'dark', name: 'Dark', color: '#1a1a1a' },
  { id: 'blue', name: 'Blue', color: '#3b82f6' },
  { id: 'purple', name: 'Purple', color: '#8b5cf6' },
] as const;
const FEATURES = [
  {
    id: 'responsive',
    name: 'Responsive Design',
    description: 'Адаптивная верстка',
  },
  { id: 'animations', name: 'Animations', description: 'CSS анимации' },
  { id: 'icons', name: 'Icons', description: 'Иконки и символы' },
  { id: 'forms', name: 'Forms', description: 'Формы обратной связи' },
  { id: 'gallery', name: 'Gallery', description: 'Галерея изображений' },
  { id: 'navigation', name: 'Navigation', description: 'Навигационное меню' },
] as const;
export default function SettingsPanel({
  isOpen,
  onClose,
  formData,
  onFormDataChange,
  livePreview,
  onLivePreviewChange,
}: SettingsPanelProps) {
  const [activeTab, setActiveTab] = useState<'style' | 'features' | 'advanced'>(
    'style'
  );
  const handleFeatureToggle = (featureId: string) => {
    const currentFeatures = formData.features || [];
    const newFeatures = currentFeatures.includes(featureId)
      ? currentFeatures.filter(f => f !== featureId)
      : [...currentFeatures, featureId];
    onFormDataChange({ ...formData, features: newFeatures });
  };
  return (
    <AnimatePresence>
      {' '}
      {isOpen && (
        <>
          {' '}
          {/* Backdrop */}{' '}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className='fixed inset-0 bg-black bg-opacity-50 z-40'
            onClick={onClose}
          />{' '}
          {/* Panel */}{' '}
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className='fixed right-0 top-0 h-full w-96 bg-[#161B22] border-l border-gray-800 z-50 flex flex-col'
          >
            {' '}
            {/* Header */}{' '}
            <div className='flex items-center justify-between p-4 border-b border-gray-800'>
              {' '}
              <div className='flex items-center space-x-2'>
                {' '}
                <Settings className='w-5 h-5' />{' '}
                <h2 className='text-lg font-semibold text-white'>
                  Settings
                </h2>{' '}
              </div>{' '}
              <button
                onClick={onClose}
                className='p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors'
              >
                {' '}
                <X className='w-5 h-5' />{' '}
              </button>{' '}
            </div>{' '}
            {/* Tabs */}{' '}
            <div className='flex border-b border-gray-800'>
              {' '}
              {[
                { id: 'style', name: 'Style', icon: Palette },
                { id: 'features', name: 'Features', icon: Zap },
                { id: 'advanced', name: 'Advanced', icon: Shield },
              ].map(tab => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 transition-colors ${activeTab === tab.id ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}
                  >
                    {' '}
                    <Icon className='w-4 h-4' />{' '}
                    <span className='text-sm font-medium'>{tab.name}</span>{' '}
                  </button>
                );
              })}{' '}
            </div>{' '}
            {/* Content */}{' '}
            <div className='flex-1 overflow-y-auto p-4 space-y-6'>
              {' '}
              {/* Style Tab */}{' '}
              {activeTab === 'style' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className='space-y-6'
                >
                  {' '}
                  <div>
                    {' '}
                    <label className='block text-sm font-medium text-gray-300 mb-3'>
                      {' '}
                      Color Theme{' '}
                    </label>{' '}
                    <div className='grid grid-cols-2 gap-2'>
                      {' '}
                      {STYLES.map(style => (
                        <button
                          key={style.id}
                          onClick={() =>
                            onFormDataChange({ ...formData, style: style.id })
                          }
                          className={`p-3 rounded-lg border transition-all ${formData.style === style.id ? 'border-blue-500 bg-blue-500/10' : 'border-gray-700 hover:border-gray-600'}`}
                        >
                          {' '}
                          <div className='flex items-center space-x-2'>
                            {' '}
                            <div
                              className='w-4 h-4 rounded'
                              style={{ backgroundColor: style.color }}
                            />{' '}
                            <span className='text-sm text-white'>
                              {style.name}
                            </span>{' '}
                          </div>{' '}
                        </button>
                      ))}{' '}
                    </div>{' '}
                  </div>{' '}
                </motion.div>
              )}{' '}
              {/* Features Tab */}{' '}
              {activeTab === 'features' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className='space-y-4'
                >
                  {' '}
                  <div>
                    {' '}
                    <label className='block text-sm font-medium text-gray-300 mb-3'>
                      {' '}
                      Additional Features{' '}
                    </label>{' '}
                    <div className='space-y-3'>
                      {' '}
                      {FEATURES.map(feature => {
                        const isEnabled =
                          formData.features?.includes(feature.id) || false;
                        return (
                          <div
                            key={feature.id}
                            className={`p-3 rounded-lg border cursor-pointer transition-all ${isEnabled ? 'border-blue-500 bg-blue-500/10' : 'border-gray-700 hover:border-gray-600'}`}
                            onClick={() => handleFeatureToggle(feature.id)}
                          >
                            {' '}
                            <div className='flex items-center justify-between'>
                              {' '}
                              <div>
                                {' '}
                                <div className='text-sm font-medium text-white'>
                                  {' '}
                                  {feature.name}{' '}
                                </div>{' '}
                                <div className='text-xs text-gray-400'>
                                  {' '}
                                  {feature.description}{' '}
                                </div>{' '}
                              </div>{' '}
                              <div
                                className={`w-4 h-4 rounded border-2 ${isEnabled ? 'bg-blue-500 border-blue-500' : 'border-gray-500'}`}
                              >
                                {' '}
                                {isEnabled && (
                                  <svg
                                    className='w-3 h-3 text-white'
                                    fill='currentColor'
                                    viewBox='0 0 20 20'
                                  >
                                    {' '}
                                    <path
                                      fillRule='evenodd'
                                      d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z'
                                      clipRule='evenodd'
                                    />{' '}
                                  </svg>
                                )}{' '}
                              </div>{' '}
                            </div>{' '}
                          </div>
                        );
                      })}{' '}
                    </div>{' '}
                  </div>{' '}
                </motion.div>
              )}{' '}
              {/* Advanced Tab */}
              {activeTab === 'advanced' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className='space-y-6'
                >
                  <div>
                    <label className='block text-sm font-medium text-gray-300 mb-3'>
                      AI Enhancement
                    </label>
                    <div className='flex items-center justify-between p-3 bg-gray-800 rounded-lg'>
                      <div>
                        <div className='text-sm font-medium text-white'>
                          AI Content Enhancement
                        </div>
                        <div className='text-xs text-gray-400'>
                          Улучшить контент с помощью ИИ
                        </div>
                      </div>
                      <button
                        onClick={() =>
                          onFormDataChange({
                            ...formData,
                            ai_enhancements: !formData.ai_enhancements,
                          })
                        }
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          formData.ai_enhancements
                            ? 'bg-blue-600'
                            : 'bg-gray-600'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            formData.ai_enhancements
                              ? 'translate-x-6'
                              : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className='block text-sm font-medium text-gray-300 mb-3'>
                      Preview Settings
                    </label>
                    <div className='flex items-center justify-between p-3 bg-gray-800 rounded-lg'>
                      <div>
                        <div className='text-sm font-medium text-white'>
                          Live Preview
                        </div>
                        <div className='text-xs text-gray-400'>
                          Автоматически обновлять предварительный просмотр
                        </div>
                      </div>
                      <button
                        onClick={() => onLivePreviewChange(!livePreview)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          livePreview ? 'bg-blue-600' : 'bg-gray-600'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            livePreview ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}
            </div>
            {/* Footer */}
            <div className='p-4 border-t border-gray-800'>
              <button
                onClick={onClose}
                className='w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors'
              >
                Apply Settings
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
