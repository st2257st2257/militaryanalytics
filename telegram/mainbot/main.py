import telebot
from telebot import types

import ast

bot = telebot.TeleBot('6819733048:AAERMFmxCbzWCx069oxrW8TYRAt-Pe49Jbw')


nameArr = ["name"]
idArr = [0]
surnameArr = ["csddc"]
ageArr = [11]
allID = 0

name = ''
surname = ''
age = 0

@bot.message_handler(content_types=['text'])
def start(message):
    global allID
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        print(message.from_user.id)
        allID += 1
        nameArr.append("")
        idArr.append(message.from_user.id)
        surnameArr.append("")
        ageArr.append(0)

        bot.register_next_step_handler(message, get_name, allID)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message, allID):  # получаем фамилию
    global name, surname
    name = message.text
    nameArr[allID] = name
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname, allID)


def get_surname(message, allID):
    global surname
    surname = message.text
    surnameArr[allID] = surname
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age, allID)


def get_age(message, allID):
    global age
    flag = ""
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
            ageArr[allID] = age
        except Exception:
            if message.text != flag:
                bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
                flag = message.text
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        print("+++")
        print(nameArr)
        print(ageArr)
        print(surnameArr)
        print(idArr)
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "no":
         print("---")


bot.polling(none_stop=True, interval=0)
