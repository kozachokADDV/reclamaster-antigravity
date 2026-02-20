# Мультиканальний Бот (Telegram, Viber, Instagram)

Цей сервер обробляє повідомлення з трьох платформ.

## Встановлення

1. Переконайтеся, що у вас встановлений Python 3.
2. Встановіть залежності:
   ```bash
   pip3 install -r requirements.txt
   ```

## Налаштування

Відкрийте файл `.env` і додайте ваші токени:

1.  **Telegram**: Отримайте токен у [@BotFather](https://t.me/BotFather).
2.  **Viber**: Створіть бота на [Viber Admin Panel](https://partners.viber.com/).
3.  **Instagram**: Потрібно створити додаток на [Facebook Developers](https://developers.facebook.com/) і підключити Instagram Graph API.

## Запуск

```bash
python3 app.py
```

Сервер запуститься на http://localhost:5000.

## Webhooks (Важливо!)

Щоб Telegram, Viber та Instagram могли надсилати повідомлення на ваш локальний комп'ютер, вам потрібна публічна адреса (HTTPS).

Використовуйте **ngrok**:
1. Завантажте ngrok.
2. Запустіть: `ngrok http 5000`
3. Скопіюйте HTTPS URL (наприклад, `https://a1b2c3d4.ngrok.io`).

### Налаштування Webhooks:

- **Telegram**:
  Відкрийте в браузері:
  `https://api.telegram.org/bot<ВАШ_ТОКЕН>/setWebhook?url=<ВАШ_NGROK_URL>/telegram`

- **Viber**:
  Потрібно відправити POST запит на налаштування (або використати скрипт).

- **Instagram**:
  Вкажіть URL Webhook у панелі Facebook розробника: `<ВАШ_NGROK_URL>/instagram`
