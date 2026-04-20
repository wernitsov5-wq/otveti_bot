import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

# ===== ТВОЙ ТОКЕН =====
BOT_TOKEN = "8712269421:AAFJnJa5flO_Te6Wm1NeNtqSr4iY11j-Uas"
CHAT_LIST_URL = "https://t.me/addlist/gvVenh7pkjs0ODZi"

# ===== НАСТРОЙКИ =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Flask веб-сервер (чтобы Render видел порт) =====
web_app = Flask('')

@web_app.route('/')
def home():
    return "✅ Бот работает!"

def run_web():
    web_app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ===== ФУНКЦИЯ СТАРТ =====
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

# ===== ЗАПУСК =====
def main():
    print("📚 БОТ ДЛЯ ОТВЕТОВ ЗАПУЩЕН")
    print("=" * 40)
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ Бот работает!")
    print(f"✅ Ссылка: {CHAT_LIST_URL}")
    print("=" * 40)
    
    app.run_polling()

if __name__ == "__main__":
    keep_alive()  # Запускаем веб-сервер (чтобы Render видел порт)
    main()        # Запускаем бота в режиме long polling
