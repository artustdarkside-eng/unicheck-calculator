# Развёртывание на Streamlit Community Cloud

## Пошаговая инструкция

### Шаг 1: Подготовка репозитория

1. Создайте публичный репозиторий на GitHub: `unicheck-calculator`
2. Загрузьте всё содержимое проекта:
   ```bash
   git add .
   git commit -m "Initial: UniCheck ROI Calculator"
   git push origin main
   ```

### Шаг 2: Регистрация на Streamlit Community Cloud

1. Перейдите на https://streamlit.io/cloud
2. Нажмите "Sign in" → "Sign up with GitHub"
3. Авторизуйте приложение Streamlit

### Шаг 3: Развёртывание приложения

1. В Streamlit Cloud нажмите "+ New app"
2. Заполните:
   - Repository: `YOUR_USERNAME/unicheck-calculator`
   - Branch: `main`
   - Main file path: `app.py`
3. Нажмите "Deploy"

Приложение будет доступно по адресу:
```
https://unicheck-calculator.streamlit.app
```

### Шаг 4: Автоматические обновления

**Как это работает:**
- Streamlit Cloud **автоматически** следит за изменениями в `main` ветке GitHub
- При каждом `git push` приложение перезагружается с новым кодом
- Обновления происходят за 30 секунд - 2 минуты

**Рабочий процесс:**

```bash
# 1. Изменяете код локально
nano app.py
# или редактируете в VS Code

# 2. Коммитите и пушите в GitHub
git add .
git commit -m "Add new feature"
git push origin main

# 3. Открываете Streamlit Cloud
# → приложение автоматически перезагружается
```

## Управление состоянием (сохранённые пресеты)

**Проблема:** Папка `saved_presets/` с пользовательскими пресетами не будет сохраняться между сеансами в Community Cloud (нет постоянного хранилища).

**Решение 1 - Database (рекомендуется):**
Добавьте интеграцию с Supabase для сохранения пресетов:

```python
# В app.py добавьте
import supabase

# Инициализируйте клиент из environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Пользовательские пресеты сохраняются в БД
```

**Решение 2 - File хранилище (простой вариант):**
Используйте Streamlit Secrets для сохранения пресетов в JSON:

```python
# В app.py
if st.button("💾 Сохранить пресет"):
    preset_data = json.dumps(params)
    # Отправьте на email или Telegram
    # или сохраните в GitHub Gist программно
```

**Решение 3 - GitHub (бесплатно, просто):**
Сохраняйте пресеты прямо в репозиторий через PyGithub:

```bash
pip install PyGithub
```

```python
from github import Github

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo("YOUR_USERNAME/unicheck-calculator")
# Сохраняйте файлы в saved_presets/ через API
```

## Переменные окружения (Secrets)

В Streamlit Cloud нажмите ⚙️ Settings → Secrets и добавьте:

```toml
# .streamlit/secrets.toml
GITHUB_TOKEN = "your_github_token_here"
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

## Мониторинг и логирование

Streamlit Cloud предоставляет логи приложения:
1. Откройте приложение на Streamlit Cloud
2. Нажмите на меню (три точки) → "Manage app"
3. Вкладка "Logs" показывает все ошибки и печать

## Масштабирование за пределы Community Cloud

Если нужны большие объёмы:

1. **Heroku** (платная опция, примерно $7/мес)
   ```bash
   pip install gunicorn
   # Создайте Procfile
   ```

2. **AWS / DigitalOcean** (от $5/мес)
   - Используйте Docker контейнер
   - Развёртывание через `docker-compose`

3. **Railway.app** (бесплатно с кредитом)
   - Автодеплой из GitHub
   - Просто выберите репозиторий

## Полезные ссылки

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Deployment Cheat Sheet](https://docs.streamlit.io/library/get-started/installation)
- [GitHub Secrets Management](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
