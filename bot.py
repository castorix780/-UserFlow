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


# ГЛАВНОЕ МЕНЮ
@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id
    args = message.text.split()

    referrer_id = None

    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1][4:])
        except ValueError:
            referrer_id = None

    if referrer_id == user_id:
        referrer_id = None

    add_user(
        user_id,
        message.from_user.username,
        message.from_user.first_name,
        referrer_id
    )

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


# РЕФЕРАЛЬНАЯ СИСТЕМА
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


# ОБРАБОТКА КНОПОК
@bot.message_handler(func=lambda message: True)
def menu(message):

    responses = {
        "🔎 SEO-анализ": "🔎 Скоро появится SEO-анализ!",
        "👥 Привлечение": "👥 Раздел привлечения пользователей.",
        "📋 Биржа заданий": "📋 Здесь будут задания.",
        "💰 Мой заработок": "💰 Здесь будет твой заработок.",
        "📊 Статистика": f"📊 Всего пользователей: {get_user_count()}",
        "👤 Профиль": f"👤 Твой ID: {message.from_user.id}"
    }

    answer = responses.get(message.text)

    if answer:
        bot.send_message(message.chat.id, answer)


# ЗАПУСК БОТА
bot.infinity_polling()
