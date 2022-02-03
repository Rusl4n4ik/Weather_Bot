import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from telebot import types

tmp = []

config_dict = get_default_config()
config_dict['language'] = 'ru'  # Локализация получаемых данных
owm = OWM('94f28a084a0b5d66b83cf1f27b3ad405', config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot('5273432675:AAGquufiioR0sBz5Bw7OIPt-eB1w0OrV7J8')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
first_btn = types.KeyboardButton("Об авторе 👨🏻‍💻")
second_btn = types.KeyboardButton("О боте 🤖")
third_btn = types.KeyboardButton("Введите город 🌏")
fourth_btn = types.KeyboardButton("Узнать погоду ⛅")
markup.add(first_btn)
markup.add(second_btn)
markup.add(third_btn)
markup.add(fourth_btn)

@bot.message_handler(commands=['start', 'help'])
def welcome_mes(message):
    bot.send_message(message.chat.id, 'Привет, я бот 🤖', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли
    if message.text == 'Об авторе 👨🏻‍💻':
        bot.send_message(message.chat.id, "Меня зовут Rusl4n4ik, 18 лет")
    if message.text == 'О боте 🤖':
        bot.send_message(message.chat.id, "Я бот созданный пользователем @Rusl4n4ik")
    if message.text == 'Введите город 🌏':
        bot.send_message(message.chat.id ,'Выберите город', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, city)
    if message.text == 'Узнать погоду ⛅':
        print(tmp)
        if tmp:
            try:
                observation = mgr.weather_at_place(tmp[0])
                w = observation.weather

                t = w.temperature("celsius")
                t1 = t['temp']
                t2 = t['feels_like']
                t3 = t['temp_max']
                t4 = t['temp_min']

                wi = w.wind()['speed']
                humi = w.humidity
                cl = w.clouds
                dt = w.detailed_status
                ti = w.reference_time('iso')
                pr = w.pressure['press']
                vd = w.visibility_distance
                bot.send_message(
                    message.chat.id,
                    "🌃  -  В городе: " + str(tmp[0]) + "\n🌡 -  Температура: " + str(t1) + " °C" + "\n" +
                    "📈  -  Максимальная температура: " + str(t3) + " °C" + "\n" +
                    "📉  -  Минимальная температура: " + str(t4) + " °C" + "\n" +
                    "🧍‍♂️  -  Ощущается как: " + str(t2) + " °C" + "\n" +
                    "💨  -  Скорость ветра: " + str(wi) + " м/с" + "\n" +
                    "📡  -  Давление: " + str(pr) + " мм.рт.ст" + "\n" +
                    "💦  -  Влажность: " + str(humi) + " %" + "\n" +
                    "👀  -  Видимость: " + str(vd) + "  метров" + "\n" +
                    "📖  -  Описание: " + str(dt))
            except:
                bot.send_message(message.chat.id, "Введите правильный город", reply_markup=markup)
                bot.register_next_step_handler(message,city)
        else:
            bot.send_message(message.chat.id, 'Вы не выбрали город', reply_markup=markup)


def city(message):
    city_name = message.text
    bot.send_message(message.chat.id, f"Вы выбрали {message.text}", reply_markup=markup)
    tmp.insert(0, city_name)

bot.polling(none_stop=True)
