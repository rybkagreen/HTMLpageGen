# 🚀 Быстрая установка HTMLPageGen для Windows

> **Простое руководство для пользователей без опыта программирования**

## 📋 Что это такое?

**HTMLPageGen** - это программа, которая помогает создавать веб-сайты с помощью искусственного интеллекта. Вы просто описываете, что хотите, а программа создает готовую веб-страницу.

## 🎯 Что вы получите:

- ✅ Веб-интерфейс для создания сайтов
- ✅ ИИ-помощник для генерации контента
- ✅ Готовые HTML-файлы для загрузки
- ✅ Работает полностью локально (без интернета)

---

## 🛠️ Установка за 15 минут

### Шаг 1: Включение WSL (Windows Subsystem for Linux)

**WSL** - это способ запустить Linux внутри Windows. Это нужно для работы программы.

1. **Нажмите** `Win + R`, введите `cmd` и нажмите `Ctrl + Shift + Enter` (запуск от администратора)

2. **Скопируйте и вставьте** эту команду:

   ```cmd
   wsl --install
   ```

3. **Перезагрузите компьютер** когда попросит

4. **После перезагрузки** откроется Ubuntu - введите:
   - **Имя пользователя** (английскими буквами, например: `john`)
   - **Пароль** (можно простой, запомните его!)

### Шаг 2: Автоматическая установка

1. **Откройте Ubuntu** (найдите в меню Пуск "Ubuntu")

2. **Скопируйте и вставьте** эту команду целиком:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/rybkagreen/HTMLpageGen/main/install.sh | bash
   ```

3. **Подождите 5-10 минут** пока всё установится

### Шаг 3: Запуск программы

После установки выполните:

```bash
cd HTMLpageGen
./start.sh
```

**🎉 Готово!** Откройте браузер и перейдите по адресу: http://localhost:3000

---

## 📖 Что делать если что-то не работает

### ❌ Ошибка "wsl command not found"

**Причина**: WSL не установлен
**Решение**:

1. Убедитесь что у вас Windows 10 версии 2004+ или Windows 11
2. Включите "Подсистему Windows для Linux" в "Компоненты Windows"

### ❌ Ubuntu не открывается

**Причина**: WSL не активирован
**Решение**:

1. Откройте PowerShell от администратора
2. Выполните: `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`
3. Перезагрузитесь

### ❌ "Permission denied" при установке

**Причина**: Нет прав доступа
**Решение**:

```bash
sudo chmod +x install.sh
./install.sh
```

### ❌ Не открывается http://localhost:3000

**Причина**: Программа не запустилась
**Решение**:

1. В Ubuntu выполните: `cd HTMLpageGen && ./start.sh`
2. Подождите 1-2 минуты
3. Попробуйте снова открыть браузер

---

## 🖥️ Как пользоваться программой

### 1. Создание первой страницы

1. **Откройте** http://localhost:3000 в браузере
2. **Нажмите** "Генератор" в меню
3. **Введите** название страницы (например: "Мой первый сайт")
4. **Опишите** что хотите (например: "Сайт про мою кошку")
5. **Нажмите** "Генерировать с ИИ"
6. **Скачайте** готовый HTML файл

### 2. Работа с ИИ-чатом

1. **Нажмите** "ИИ Чат" в меню
2. **Задайте вопрос** (например: "Как сделать красивую кнопку?")
3. **Получите** подробный ответ от ИИ

### 3. Сохранение результатов

- Все созданные файлы сохраняются в папку `Загрузки`
- Можете открыть их в любом браузере
- Можете загрузить на хостинг для публикации в интернете

---

## 🔧 Полезные команды

### Запуск программы

```bash
cd HTMLpageGen && ./start.sh
```

### Остановка программы

Нажмите `Ctrl + C` в терминале Ubuntu

### Обновление программы

```bash
cd HTMLpageGen
git pull
./start.sh
```

### Полная переустановка

```bash
rm -rf HTMLpageGen
curl -fsSL https://raw.githubusercontent.com/rybkagreen/HTMLpageGen/main/install.sh | bash
```

---

## 📞 Поддержка

Если ничего не помогает:

1. **Сделайте скриншот** ошибки
2. **Опишите** что делали когда произошла ошибка
3. **Напишите** разработчику: [GitHub Issues](https://github.com/rybkagreen/HTMLpageGen/issues)

---

## 💡 Полезные советы

- **Всегда запускайте** программу через Ubuntu, не через Windows
- **Не закрывайте** окно Ubuntu пока пользуетесь программой
- **Если что-то зависло** - перезапустите Ubuntu и попробуйте снова
- **Сохраняйте** важные результаты в отдельную папку

**🎉 Удачного использования!**
