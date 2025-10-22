# 🚀 Развёртывание на Streamlit Community Cloud за 5 минут

## Что вам нужно:
- ✅ GitHub аккаунт
- ✅ Streamlit аккаунт (можно через GitHub)
- ✅ 5 минут времени

---

## Шаг 1️⃣: Создайте репозиторий на GitHub

```bash
# На вашем компьютере
cd ~/Desktop/Unicheck/onlcalc

# Создайте публичный репозиторий на github.com
# Назовите его: unicheck-calculator

# Загрузите код:
git remote add origin https://github.com/YOUR_USERNAME/unicheck-calculator.git
git branch -M main
git push -u origin main
```

---

## Шаг 2️⃣: Разверните на Streamlit Cloud

1. Перейдите на https://streamlit.io/cloud
2. Нажмите **"+ New app"**
3. Заполните поля:
   - **Repository:** `YOUR_USERNAME/unicheck-calculator`
   - **Branch:** `main`
   - **Main file:** `app.py`
4. Нажмите **"Deploy"** ✨

Готово! Приложение будет доступно через ~2 минуты на:
```
https://unicheck-calculator.streamlit.app
```

---

## Шаг 3️⃣: Работайте локально, обновления идут в облако

**Изменяете код** → **Git push** → **Автоматическое обновление** ✅

```bash
# Измените что-то в app.py
nano app.py

# Запушьте в GitHub
git add .
git commit -m "Улучшение интерфейса"
git push origin main

# Через 30 сек - 2 мин приложение обновится автоматически!
```

---

## Что дальше?

- 📖 **Подробная инструкция** → смотрите `DEPLOYMENT.md`
- 🔑 **Secrets & Variables** → нужны для сохранения пресетов в БД
- 📊 **Мониторинг логов** → в меню приложения на Streamlit Cloud

---

## Часто задаваемые вопросы

**Q: Что если у меня нет GitHub?**  
A: Создайте бесплатный аккаунт на github.com за 2 минуты

**Q: Будет ли работать на мобильном?**  
A: Да! Streamlit автоматически адаптируется под все экраны

**Q: Можно ли добавить пароль?**  
A: Да, через `st.secrets` → сохраняйте пароль в Streamlit Cloud Secrets

**Q: Что с пользовательскими пресетами?**  
A: Сейчас они хранятся локально. Для облака нужна БД (Supabase, PostgreSQL)

---

Вопросы? Смотрите `DEPLOYMENT.md` для полной документации 📚
