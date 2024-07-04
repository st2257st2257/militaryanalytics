import requests
from config import notAuth, \
    isAuth, \
    mainMenu, \
    urlAdress, \
    urlBase

import ast
import telebot
from telebot import types

bot = telebot.TeleBot('6819733048:AAERMFmxCbzWCx069oxrW8TYRAt-Pe49Jbw')

globalActions = ["/start", "/mainMenu"]

name = ''
surname = ''
age = 0
userIdCur = 0


def sendRequest(actionType, userId, fieldNM="", value=""):
    data = {}
    if actionType == "addNew":
        data = {'actionType': "addNew",
                'userId': userId}
    elif actionType == "editField":
        data = {'actionType': "editField",
                'userId': userId,
                'fieldNM': fieldNM,
                'value': value}
    elif actionType == "getUserData":
        data = {'actionType': "getUserData",
                'userId': userId}
        return requests.post(urlAdress + '/tgbot/', data=data)
    requests.post(urlAdress + '/tgbot/', data=data)


def globalFun(message, userId=0):
    if userId == 0:
        bot.send_message(message.from_user.id, mainMenu)
        print(message.text)
    else:
        bot.send_message(userId, mainMenu)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        print(message.from_user.id)

        sendRequest("addNew", message.from_user.id)

        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        answer = str(sendRequest("getUserData", message.from_user.id).content)[2:-1]
        data = ast.literal_eval(answer)
        if data["type"] == "True":
            if message.text in globalActions:
                globalFun(message)
            else:
                bot.send_message(message.from_user.id, isAuth)
        elif data["type"] == "False":
            bot.send_message(message.from_user.id, notAuth)


def get_name(message):
    global name, surname
    if message.text in globalActions:
        globalFun(message)
    else:
        name = message.text
        sendRequest("editField", message.from_user.id, fieldNM="firstNM", value=name)
        bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
        bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    if message.text in globalActions:
        globalFun(message)
    else:
        surname = message.text
        sendRequest("editField", message.from_user.id, fieldNM="secondNM", value=surname)
        bot.send_message(message.from_user.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age, userIdCur
    if message.text in globalActions:
        globalFun(message)
    else:
        flag = ""
        while age == 0:  # проверяем что возраст изменился
            try:
                age = int(message.text)  # проверяем, что возраст введен корректно
                sendRequest("editField", message.from_user.id, fieldNM="age", value=age)
            except Exception as e:
                print(e)
                if message.text != flag:
                    bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
                    flag = message.text
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
        userIdCur = message.from_user.id
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.message.text in globalActions:
        globalFun(call.message)
    else:
        if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
            print("+++")
            # sendRequest("editField", call.message.from_user.id, fieldNM="rightData", value="Yes")
            bot.send_message(call.message.chat.id, 'Вы успешно зарегистированы')
            globalFun(call.message, userIdCur)
        elif call.data == "no":
            print("---")
            # sendRequest("editField", call.message.from_user.id, fieldNM="rightData", value="No")


bot.polling(none_stop=True, interval=0)
