## TG First Comment Bot (aiogram3)

Бот оставляет первый комментарий под каждым новым постом в канале (в привязанной группе обсуждений).

### Запуск

1) python -m venv .venv
2) source .venv/bin/activate (Linux/macOS) или .venv\Scripts\activate (Windows)
3) pip install -U pip
4) pip install -e .
5) cp .env.example .env и заполнить BOT_TOKEN и т.д.
6) python -m src.app.main

### Требования в Telegram

- Канал должен быть привязан к discussion group
- Бот админ в канале и имеет право писать в группе
