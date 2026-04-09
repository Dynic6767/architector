import telebot
from logic import api
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я создаю картинки, спроси меня."
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    image_path = f"generated_image_{message.chat.id}.jpg"
    api.gen_image(prompt, image_path)
    with open(image_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

bot.polling()
