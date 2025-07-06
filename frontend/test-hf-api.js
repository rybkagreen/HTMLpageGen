// Тестовый скрипт для проверки Hugging Face API
// Запуск: node test-hf-api.js

const fetch = require('node-fetch');

const HF_TOKEN = process.env.HF_TOKEN || 'your_hugging_face_token_here';

async function testHuggingFaceAPI() {
  console.log('🚀 Тестирование Hugging Face API...');
  console.log('📍 URL: https://router.huggingface.co/featherless-ai/v1/chat/completions');
  console.log('🤖 Модель: deepseek-ai/DeepSeek-R1-Distill-Qwen-14B');
  
  if (HF_TOKEN === 'your_hugging_face_token_here') {
    console.log('❌ Установите переменную окружения HF_TOKEN');
    console.log('   export HF_TOKEN=your_actual_token');
    return;
  }

  try {
    const response = await fetch('https://router.huggingface.co/featherless-ai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${HF_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [
          {
            role: 'user',
            content: 'Создай простую HTML страницу с заголовком "Привет, мир!" и стилями CSS'
          }
        ],
        model: 'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B',
        stream: false,
        temperature: 0.7,
        max_tokens: 1000
      })
    });

    console.log(`📊 Статус ответа: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      const errorText = await response.text();
      console.log('❌ Ошибка API:', errorText);
      return;
    }

    const data = await response.json();
    console.log('✅ Успешный ответ!');
    console.log('📝 Содержимое ответа:');
    console.log(data.choices[0].message.content);
    
    if (data.usage) {
      console.log('📈 Использование токенов:', data.usage);
    }

  } catch (error) {
    console.log('❌ Ошибка при запросе:', error.message);
  }
}

// Также тестируем локальный API роут
async function testLocalAPI() {
  console.log('\n🏠 Тестирование локального API роута...');
  
  try {
    const response = await fetch('http://localhost:3000/api/huggingface', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [
          {
            role: 'user',
            content: 'Создай HTML страницу для портфолио'
          }
        ],
        stream: false,
        temperature: 0.7,
        max_tokens: 1000
      })
    });

    console.log(`📊 Статус ответа: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      const errorData = await response.json();
      console.log('❌ Ошибка локального API:', errorData);
      return;
    }

    const data = await response.json();
    console.log('✅ Локальный API работает!');
    
    if (data.success) {
      console.log('📝 Ответ AI:', data.message.substring(0, 200) + '...');
    } else {
      console.log('❌ API ошибка:', data.message);
    }

  } catch (error) {
    console.log('❌ Локальный сервер недоступен:', error.message);
    console.log('💡 Запустите: npm run dev');
  }
}

async function main() {
  console.log('🧪 Запуск тестов Hugging Face API\n');
  
  // Тест прямого API
  await testHuggingFaceAPI();
  
  // Тест локального роута
  await testLocalAPI();
  
  console.log('\n✨ Тестирование завершено!');
}

main().catch(console.error);
