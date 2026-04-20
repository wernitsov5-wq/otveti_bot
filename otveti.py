import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os

# ===== ТВОЙ ТОКЕН =====
BOT_TOKEN = "8712269421:AAFJnJa5flO_Te6Wm1NeNtqSr4iY11j-Uas"
CHAT_LIST_URL = "https://t.me/addlist/gvVenh7pkjs0ODZi"

logging.basicConfig(level=logging.INFO)

# Flask веб-сервер
web_app = Flask('')

@web_app.route('/')
def home():
    return "✅ Бот работает!"

@web_app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot_app.bot)
    bot_app.update_queue.put(update)
    return 'ok', 200

# Асинхронная функция start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    
    text = (
        f"📚 **ОТВЕТЫ МЦКО ВПР 2026** 📚\n\n"
        f"Привет, {user_name}!\n\n"
        f"✅ **Вот ссылка на ответы:**\n"
        f"{CHAT_LIST_URL}\n\n"
        f"📌 **Что там есть:**\n"
        f"• ВПР 4, 5, 6, 7, 8 класс\n"
        f"• МЦКО все классы\n"
        f"• Итоговые сочинения\n"
        f"• Олимпиадные задания\n\n"
        f"🔥 Переходи и пользуйся!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 ПОЛУЧИТЬ ОТВЕТЫ", url=CHAT_LIST_URL)],
        [InlineKeyboardButton("👥 ПОДЕЛИТЬСЯ", switch_inline_query=f"Вот ссылка на ответы: {CHAT_LIST_URL}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

# Запуск
def main():
    global bot_app
    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    
    # Устанавливаем веб-хук (один раз при запуске)
    webhook_url = f"https://otveti-bot.onrender.com/webhook/{BOT_TOKEN}"
    bot_app.bot.set_webhook(webhook_url)
    
    print("📚 БОТ ЗАПУЩЕН")
    print(f"✅ Веб-хук: {webhook_url}")
    
    # Запускаем Flask
    web_app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    main()