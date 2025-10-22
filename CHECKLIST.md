# ✅ Чеклист перед деплоем на Streamlit Cloud

## Основное

- [x] Проект инициализирован как Git репозиторий
- [x] Файл `requirements.txt` содержит все зависимости:
  - streamlit >= 1.28.0
  - pandas >= 2.0.0
  - plotly >= 5.0.0
- [x] Основной файл приложения: `app.py` (работает локально с `streamlit run app.py`)
- [x] `.streamlit/config.toml` создан с базовой конфигурацией
- [x] `.gitignore` создан для игнорирования ненужных файлов

## Документация

- [x] `README.md` - описание проекта
- [x] `DEPLOYMENT.md` - полная инструкция развёртывания
- [x] `QUICKSTART_DEPLOY.md` - быстрый старт за 5 минут

## Обработка ошибок

- [x] Импорты в `app.py` проверены (используются `plotly.graph_objects`, `pandas`, `streamlit`)
- [x] Функции в `calc.py` работают корректно
- [x] Форматирование денег/процентов работает (`formatters.py`)

## Перед первым пушем

```bash
# Убедитесь, что локально работает
streamlit run app.py

# Проверьте, что всё коммитится
git status

# Если всё хорошо:
git log --oneline
```

## После создания репозитория на GitHub

```bash
# Замените YOUR_USERNAME на ваше имя пользователя GitHub
git remote set-url origin https://github.com/YOUR_USERNAME/unicheck-calculator.git
git branch -M main
git push -u origin main
```

## На Streamlit Cloud

1. Авторизуйтесь через GitHub на https://streamlit.io/cloud
2. Нажмите "+ New app"
3. Выберите ваш репозиторий: `YOUR_USERNAME/unicheck-calculator`
4. Main file: `app.py`
5. Deploy!

## Особенности Streamlit Community Cloud

✅ **Включено:**
- Автоматический деплой при git push
- HTTPS и SSL
- Custom domain (платная опция)
- Бесплатный хостинг

⚠️ **Ограничения:**
- Нет постоянного хранилища файлов (saved_presets/ будут сброшены)
- Максимум 1GB памяти на приложение
- Перезапуск при обновлении кода
- Скрипт выполняется заново при каждой переоди пользователя

## Сохранение пользовательских пресетов (важно!)

Сейчас пресеты сохраняются в `saved_presets/` локально, но в облаке это не работает.

**Решение - выберите одно:**

### Вариант 1: Email/Telegram (самый простой)
Добавьте кнопку "Отправить пресет на email":
```python
if st.button("📧 Отправить пресет"):
    # Используйте smtplib или Telegram API
    pass
```

### Вариант 2: Supabase (рекомендуется, бесплатно)
```bash
pip install supabase
```
Сохраняйте пресеты в облачную БД

### Вариант 3: GitHub Gist (для текстовых пресетов)
```bash
pip install PyGithub
```

## После развёртывания

1. Откройте приложение в браузере
2. Проверьте, что все функции работают
3. Попробуйте экспортировать CSV
4. Попробуйте шарить ссылку с параметрами

## Полезные команды

```bash
# Просмотр логов локально
streamlit logger configure

# Запуск с дополнительной отладкой
streamlit run app.py --logger.level=debug

# Обновить зависимости
pip install -U -r requirements.txt
```

## Если что-то не работает

1. Откройте https://[YOUR-APP].streamlit.app/
2. Нажмите на меню (три точки) → "Manage app"
3. Вкладка "Logs" показывает ошибки
4. Обычные проблемы:
   - Забыли добавить зависимость в `requirements.txt`
   - Ошибка в импортах Python
   - Локальный файл не загружен в GitHub

## Масштабирование

Если нужны большие объёмы:
- **Docker** для AWS, GCP, Azure
- **Railway.app** для простого хостинга
- **Heroku** (платный, но простой)

Но для начала Community Cloud - идеален! 🚀
