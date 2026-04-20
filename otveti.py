import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os

# ===== ТВОЙ ТОКЕН =====
BOT_TOKEN = "8712269421:AAFJnJa5flO_Te6Wm1NeNtqSr4iY11j-Uas"
CHAT_LIST_URL = "https://t.me/addlist/gvVenh7pkjs0ODZi"

# ===== НАСТРОЙКИ =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== ИНИЦИАЛИЗАЦИЯ БОТА =====
bot_app = Application.builder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# ===== Flask веб-сервер =====
web_app = Flask('')

@web_app.route('/')
def home():
    return "✅ Бот работает!"

@web_app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def webhook():
    """Принимает обновления от Telegram и передает их боту."""
    try:
        update = Update.de_json(request.get_json(), bot_app.bot)
        bot_app.process_update(update)
        return 'ok', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке веб-хука: {e}")
        return 'error', 500

# ===== ФУНКЦИЯ СТАРТ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    
    text = (
        f"📚 **ОТВЕТЫ ВПР МЦКО 2026** 📚\n\n"
        f"Привет, {user_name}!\n\n"
        f"✅ **Вот ссылка на ответы:**\n"
        f"{CHAT_LIST_URL}\n\n"
        f"📌 **Что там есть:**\n"
        f"• ВПР 4, 5, 6, 7, 8 и 10 класс\n"
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
if __name__ == "__main__":
    print("📚 БОТ ЗАПУЩЕН И ГОТОВ К РАБОТЕ ЧЕРЕЗ ВЕБ-ХУК")
    web_app.run(host='0.0.0.0', port=10000)