# Blog Platform (Django)

Учебный проект на Django: блог с постами, настройками пользователя через cookies (тема, язык, последние посещённые), внешними стилями и адаптивной вёрсткой.

## Возможности
- Главная с карточками постов и hero-секцией.
- Детальная страница поста.
- Создание поста через форму (заголовок, содержимое, категория, изображение).
- Настройки пользователя: тема (light/dark), язык (EN/RU), предпочитаемые категории — хранятся в cookies.
- Список последних посещённых постов (cookies).
- Внешние стили: `static/css/styles.css` и `static/css/dark.css`.

## Требования
- Python 3.11+
- pip

## Установка и запуск (Windows)
1. Клонировать репозиторий:
   - Откройте терминал в удобной папке и вы��олните:
     ```bash
     git clone https://github.com/<YOUR_USERNAME>/blog_platform.git
     cd blog_platform
     ```

2. Создать и активировать виртуальное окружение:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустить сервер разработки:
   ```bash
   python manage.py runserver
   ```

5. Открыть в браузере:
   - Главная: http://127.0.0.1:8000/

## Структура проекта (основное)
- `blog_platform/` — настройки проекта и urls
- `blog_app/` — приложение: views, templates
- `static/css/` — стили (light/dark)
- `static/images/` — изображения (включая placeholder `default.svg` и изображения постов `tech.svg`, `lifestyle.svg`, `travel.svg`)

## Cookies и пользовательские настройки
- Тема: cookie `theme` (light|dark)
- Язык: cookie `language` (EN|RU)
- Предпочитаемые категории: cookie `categories` (CSV)
- Последние посещённые: cookie `last_visited` (JSON-массив ID постов)
- Настройки читаются и применяются ко всем страницам (см. `get_user_prefs` в `blog_app/views.py`).

## Данные
В проекте данные постов заданы прямо в коде (`blog_app/views.py`, список `posts`). При создании поста загруженное изображение сохраняется в `static/images/`; если изображение не загружено — используется `default.svg`.

## Тестирование (ручное)
- Preferences: выберите тёмную тему и RU, сохраните — проверьте все страницы.
- Last Visited: откройте несколько постов, проверьте блок «Последние посещенные» на главной.
- Создание поста: создайте пост без изображения — отобразится `default.svg`.
- Адаптивность: сузьте окно браузера до < 900px.

## Git и публикация
1. Инициализация репозитория и первый коммит:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Django blog with cookies, themes, and styling"
   git branch -M main
   ```
2. Создайте пустой репозиторий на GitHub: `blog_platform`.
3. Свяжите и запушьте:
   ```bash
   git remote add origin https://github.com/<YOUR_USERNAME>/blog_platform.git
   git push -u origin main
   ```

## Примечания
- Если Edge показывает старые стили — сделайте жесткую перезагрузку (Ctrl+F5) или отключите кэш в DevTools → Network → Disable cache.
- Для продакшена используйте `collectstatic` и хеширование статики (ManifestStaticFilesStorage).
