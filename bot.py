import telebot
import os
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не настроен")

bot = telebot.TeleBot(TOKEN)

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
