import telebot
from logic import api
from config import token
import os

bot = telebot.TeleBot(token)
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я создаю картинки, спроси меня."
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Вот мои команды: /hello, /bye, /calculator, /stop, /remind.")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    user_states[message.chat.id] = 'waiting_for_feedback'

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == 'waiting_for_feedback')
def handle_response(message):
    if message.text.lower() == "хорошо":
        bot.reply_to(message, "Очень хорошо слышать, создай картинку, вписывая свой промпт")
        user_states.pop(message.chat.id)
    elif message.text.lower() == "плохо":
        bot.reply_to(message, "Извините, это очень грустно слышать, желаем вам лучшего")
        user_states.pop(message.chat.id)

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи! Успехов с вашей картинкой")

@bot.message_handler(commands=['calculator'])
def start_calculator(message):
    global is_calculator_active
    is_calculator_active = True
    bot.reply_to(message, "Привет! Я могу быть калькулятором, напишите пример или /stop2, чтобы остановить.")

@bot.message_handler(commands=['stop'])
def stop_calculator(message):
    global is_calculator_active
    is_calculator_active = False
    bot.reply_to(message, "Калькулятор остановлен. Если хотите снова использовать калькулятор, введите команду /calculator.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    image_path = f"generated_image_{message.chat.id}.jpg"

    try:
        file_to_send = api.gen_image(prompt, image_path)

        with open(file_to_send, "rb") as photo:
            bot.send_photo(message.chat.id, photo)

        if os.path.exists(file_to_send):
            os.remove(file_to_send)
            print(f"Файл {file_to_send} удалён")

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка, сорян бро")
        print(f"Ошибка: {e}")

bot.polling()
