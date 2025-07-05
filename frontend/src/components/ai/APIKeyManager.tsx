'use client';

import { useEffect, useState } from 'react';

export interface APIKeySettings {
  huggingfaceKey: string;
  useDirectClient: boolean;
}

interface APIKeyManagerProps {
  onSettingsChange: (settings: APIKeySettings) => void;
  initialSettings?: APIKeySettings;
}

export default function APIKeyManager({
  onSettingsChange,
  initialSettings,
}: APIKeyManagerProps) {
  const [settings, setSettings] = useState<APIKeySettings>({
    huggingfaceKey: '',
    useDirectClient: true,
    ...initialSettings,
  });

  const [showKey, setShowKey] = useState(false);
  const [keyStatus, setKeyStatus] = useState<'unknown' | 'valid' | 'invalid'>(
    'unknown'
  );

  useEffect(() => {
    // Загружаем настройки из localStorage
    const savedSettings = localStorage.getItem('deepseek-api-settings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings(prev => ({ ...prev, ...parsed }));
      } catch (error) {
        console.error('Error loading saved settings:', error);
      }
    }
  }, []);

  const handleSettingsUpdate = (newSettings: Partial<APIKeySettings>) => {
    const updated = { ...settings, ...newSettings };
    setSettings(updated);

    // Сохраняем в localStorage
    localStorage.setItem('deepseek-api-settings', JSON.stringify(updated));

    // Уведомляем родительский компонент
    onSettingsChange(updated);
  };

  const handleKeyValidation = async () => {
    if (!settings.huggingfaceKey.trim()) {
      setKeyStatus('invalid');
      return;
    }

    try {
      // Простая проверка формата ключа
      if (
        settings.huggingfaceKey.startsWith('hf_') &&
        settings.huggingfaceKey.length > 10
      ) {
        setKeyStatus('valid');
      } else {
        setKeyStatus('invalid');
      }
    } catch (error) {
      setKeyStatus('invalid');
    }
  };

  useEffect(() => {
    handleKeyValidation();
  }, [settings.huggingfaceKey]);

  return (
    <div className='bg-white rounded-lg border border-gray-200 p-4'>
      <h3 className='text-lg font-semibold text-gray-900 mb-4'>
        Настройки DeepSeek AI
      </h3>

      <div className='space-y-4'>
        {/* API Key Input */}
        <div>
          <label className='block text-sm font-medium text-gray-700 mb-2'>
            Hugging Face API Key
          </label>
          <div className='relative'>
            <input
              type={showKey ? 'text' : 'password'}
              value={settings.huggingfaceKey}
              onChange={e =>
                handleSettingsUpdate({ huggingfaceKey: e.target.value })
              }
              placeholder='hf_...'
              className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 pr-20'
            />
            <button
              type='button'
              onClick={() => setShowKey(!showKey)}
              className='absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700'
            >
              {showKey ? '🙈' : '👁️'}
            </button>
          </div>

          {/* Key Status */}
          <div className='mt-1 flex items-center gap-2'>
            <div
              className={`w-2 h-2 rounded-full ${
                keyStatus === 'valid'
                  ? 'bg-green-500'
                  : keyStatus === 'invalid'
                    ? 'bg-red-500'
                    : 'bg-gray-300'
              }`}
            />
            <span
              className={`text-xs ${
                keyStatus === 'valid'
                  ? 'text-green-600'
                  : keyStatus === 'invalid'
                    ? 'text-red-600'
                    : 'text-gray-500'
              }`}
            >
              {keyStatus === 'valid'
                ? 'Ключ корректный'
                : keyStatus === 'invalid'
                  ? 'Ключ некорректный'
                  : 'Статус неизвестен'}
            </span>
          </div>
        </div>

        {/* Client Mode Toggle */}
        <div>
          <label className='flex items-center'>
            <input
              type='checkbox'
              checked={settings.useDirectClient}
              onChange={e =>
                handleSettingsUpdate({ useDirectClient: e.target.checked })
              }
              className='rounded border-gray-300 text-blue-600 focus:ring-blue-500'
            />
            <span className='ml-2 text-sm text-gray-700'>
              Использовать прямое подключение к Hugging Face
            </span>
          </label>
          <p className='text-xs text-gray-500 mt-1'>
            {settings.useDirectClient
              ? 'Запросы будут отправляться напрямую в Hugging Face (быстрее, но требует API ключ)'
              : 'Запросы будут обрабатываться через backend сервер (медленнее, но безопаснее)'}
          </p>
        </div>

        {/* Help Text */}
        <div className='bg-blue-50 p-3 rounded-md'>
          <h4 className='text-sm font-medium text-blue-900 mb-1'>
            Как получить API ключ:
          </h4>
          <ol className='text-xs text-blue-800 list-decimal list-inside space-y-1'>
            <li>
              Зайдите на{' '}
              <a
                href='https://huggingface.co/settings/tokens'
                target='_blank'
                rel='noopener noreferrer'
                className='underline'
              >
                huggingface.co/settings/tokens
              </a>
            </li>
            <li>Создайте новый токен с правами "Read"</li>
            <li>Скопируйте токен и вставьте выше</li>
          </ol>
        </div>

        {/* Current Status */}
        <div className='text-xs text-gray-500 space-y-1'>
          <div>Модель: deepseek-ai/DeepSeek-V3</div>
          <div>
            Режим:{' '}
            {settings.useDirectClient ? 'Прямое подключение' : 'Через backend'}
          </div>
          <div>
            Статус:{' '}
            {keyStatus === 'valid'
              ? '✅ Готов к работе'
              : '❌ Требуется настройка'}
          </div>
        </div>
      </div>
    </div>
  );
}
