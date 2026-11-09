import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🚀 Добро пожаловать в UserFlow!\n\n"
        "Платформа для продвижения и аналитики Telegram."
    )

bot.infinity_polling()
