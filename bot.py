import telebot
import os
from telebot import types
from database import (
    init_db,
    add_user,
    get_user_count,
    get_referral_count
)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не настроен")

bot = telebot.TeleBot(TOKEN)
init_db()
@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    keyboard.row("🔎 SEO-анализ", "👥 Привлечение")
    keyboard.row("📋 Биржа заданий", "💰 Мой заработок")
    keyboard.row("📊 Статистика", "👤 Профиль")

    bot.send_message(
        message.chat.id,
        "🚀 Добро пожаловать в USERFLOW!\n\n"
        "Платформа для продвижения Telegram-проектов.\n\n"
        "Выбери нужный раздел:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: True)
def menu(message):

    responses = {
        "🔎 SEO-анализ": "🔎 Скоро здесь появится SEO-анализ каналов!",
        "👥 Привлечение": "👥 Раздел привлечения пользователей.",
        "📋 Биржа заданий": "📋 Здесь будут доступны задания.",
        "💰 Мой заработок": "💰 Здесь будет отображаться твой заработок.",
        "📊 Статистика": "📊 Здесь появится статистика.",
        "👤 Профиль": "👤 Твой профиль UserFlow."
    }

    answer = responses.get(message.text)

    if answer:
        bot.send_message(message.chat.id, answer)


bot.infinity_polling()
@bot.message_handler(commands=['referral'])
def referral(message):
    user_id = message.from_user.id
    bot_username = bot.get_me().username

    link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    count = get_referral_count(user_id)

    bot.send_message(
        message.chat.id,
        f"👥 Твоя реферальная система\n\n"
        f"🔗 Твоя ссылка:\n{link}\n\n"
        f"👤 Приглашено: {count}"
    )
