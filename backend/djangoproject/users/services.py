# @Aleksandr Kristal v0.0.1 || create all
from typing import Dict
import ast
from app1.config import \
    dictStatus
from app1.config import \
    password_recovery, \
    password_recovery_title, \
    getRandomCode, \
    dictStatus
from users.models import \
    User
from app1.models import \
    UserFile
from app1.views import \
    sendEmail, \
    sendEmailRecovery, \
    sendRegProofEmail
import os
import shutil
from datetime import datetime
from users.models import Chat, Message, getToken, User

def get_user_token(login: str, password: str):
    flag = User.objects.filter(login=login,
                               password=password)
    if len(flag) == 0:
        return {"result": dictStatus.get(111),
                "name": login}
    elif len(flag) == 1:
        current_user = User.objects.get(login=login)
        current_user.token = getToken(login)
        current_user.save()
        return {"result": True,
                "name": login,
                "token": getToken(login)}
    else:
        return {"result": dictStatus.get(111)}


def update_files():
    src = 'media/messages'
    trg = 'static/messages'
    files = os.listdir(src)
    for fileName in files:
        shutil.copy2(os.path.join(src, fileName), trg)


def get_all_sellers():
    res = {"result": True}
    seller_list = User.objects.filter(userRole="seller")
    for seller in seller_list:
        company_logo = ""
        files_list = UserFile.objects.filter(user_owner=seller.login,
                                             file_name="company_logo")
        if len(files_list) > 0:
            company_logo = files_list[0].file_static_url
            fullDescription = seller.fullDescription
            companyName = seller.companyName

            if seller.fullDescription != "" and \
                    companyName != "" and \
                    fullDescription != "":
                res[seller.login] = {
                    "completeness": check_completeness(seller.login),
                    "login": seller.login,
                    "company_name": seller.companyName,
                    "fullDescription": fullDescription,
                    "company_logo": company_logo
                }
    return res


def send_recovery_link(login: str) -> Dict[str, any]:
    flag = User.objects.filter(login=login)
    if len(flag) == 0:
        return {"result": dictStatus.get(111),
                "name": login}
    elif len(flag) == 1:
        user = User.objects.get(login=login)
        user.emailRecoveryToken = getRandomCode(9)
        sendEmailRecovery(password_recovery_title,
                          password_recovery,
                          user.email,
                          user.emailRecoveryToken)
        user.save()
        return {"result": True,
                "login": login,
                "tokenRecovery": user.emailRecoveryToken}

def get_recovery_link(token: str, pass1: str, pass2: str) -> Dict[str, any]:
    flag = User.objects.filter(emailRecoveryToken=token)
    if len(flag) == 0:
        return {"result": dictStatus.get(111),
                "token": token}
    elif len(flag) == 1:
        user = User.objects.get(emailRecoveryToken=token)
        if pass1 == pass2:
            user.password = pass1
            user.save()
            return {"login": user.login,
                    "result": True,
                    "token": user.token}
        else:
            return {"result": dictStatus.get(111),
                    "token": token}
    else:
        return {"result": dictStatus.get(111)}


def send_email(title: str, text: str, email: str) -> Dict[str, any]:
    sendEmail(title,
              text,
              email)
    return {"result": True,
            "email": email,
            "title": title}


def create_chat(first_user_login: str, second_user_login: str) -> Dict[str, any]:
    """Создание чата"""
    if len(Chat.objects.filter(firstUserLogin=first_user_login,
                               secondUserLogin=second_user_login)) > 0:
        chat = Chat.objects.filter(firstUserLogin=first_user_login,
                                   secondUserLogin=second_user_login)[0]
        return {"result": True,
                "opponentName": chat.secondUserName,
                "Id": chat.id}
    elif len(Chat.objects.filter(firstUserLogin=second_user_login,
                                 secondUserLogin=first_user_login)) > 0:
        chat = Chat.objects.filter(firstUserLogin=second_user_login,
                                   secondUserLogin=first_user_login)[0]
        return {"result": True,
                "opponentName": chat.firstUserLogin,
                "Id": chat.id}
    else:
        fun = User.objects.get(login=first_user_login).firstNM
        sun = User.objects.get(login=second_user_login).firstNM
        new_chat = Chat(firstUserLogin=first_user_login,
                        secondUserLogin=second_user_login,
                        firstUserName=fun,
                        secondUserName=sun,
                        visibility=1)
        new_chat.save()
        return {"result": True,
                "opponentName": new_chat.secondUserName,
                "Id": new_chat.id}


def get_not_read(chat_id: int, first_user_login: str):
    chat_messages = Message.objects.filter(chatId=chat_id)
    is_read = 0
    number_of_not_read = 0
    for message in chat_messages:
        if message.notRead == 1 and \
                message.ownerLogin != first_user_login:
            is_read = 1
            number_of_not_read += 1
    return is_read, number_of_not_read


def read_message(first_user_login: str, message_id: int):
    message_obj = Message.objects.filter(id=message_id)
    if len(message_obj) == 1:
        message = Message.objects.get(id=message_id)
        if message.ownerLogin != first_user_login:
            message.notRead = 0
            message.save()
    return {"result": True}


def read_chat(first_user_login: str, chat_id: int):
    chat_obj = Message.objects.filter(id=chat_id)
    if len(chat_obj) == 1:
        messages = Message.objects.filter(chatId=chat_id)
        for message in messages:
            read_message(first_user_login, message.id)
    return {"result": True}


def get_chats(first_user_login: str) -> Dict[str, any]:
    """Получение чатов пользователя"""
    chats_first = Chat.objects.filter(firstUserLogin=first_user_login)
    chats_second = Chat.objects.filter(secondUserLogin=first_user_login)
    ans = {"allForRead": 0}
    for chat in chats_first:
        not_read, number_of_messages = get_not_read(chat.id, first_user_login)
        ans["allForRead"] += not_read
        ans[chat.id] = {"chatId": chat.id,
                        "firstUserLogin": chat.firstUserLogin,
                        "firstUserName": chat.firstUserName,
                        "firstCompanyName": _get_company_name(chat.firstUserLogin),
                        "secondUserName": chat.secondUserName,
                        "secondUserLogin": chat.secondUserLogin,
                        "secondCompanyName": _get_company_name(chat.secondUserLogin),
                        "visibility": chat.visibility,
                        "notRead": not_read,
                        "numberOfMessages": number_of_messages}
    for chat in chats_second:
        not_read, number_of_messages = get_not_read(chat.id, first_user_login)
        ans["allForRead"] += not_read
        ans[chat.id] = {"chatId": chat.id,
                        "firstUserLogin": chat.firstUserLogin,
                        "secondUserLogin": chat.secondUserLogin,
                        "firstUserName": chat.firstUserName,
                        "secondUserName": chat.secondUserName,
                        "firstCompanyName": _get_company_name(chat.firstUserLogin),
                        "secondCompanyName": _get_company_name(chat.secondUserLogin),
                        "visibility": chat.visibility,
                        "notRead": not_read,
                        "numberOfMessages": number_of_messages}
    return ans


def get_chat_messages(chat_id: int) -> Dict[str, any]:
    """Получение сообщений конкретного чата"""
    res = Message.objects.filter(chatId=chat_id)
    ans = {}
    for i in range(len(res)):
        message = res[i]
        url = ""
        if message.data:
            url = os.getenv('DJANGO_BACKEND_URL', 'http://127.0.0.1:8000') + "/static" + \
                    str(message.data.url)[6:]
        ans[str(message.id)] = {
            "text": message.text,
            "date": message.date,
            "ownerLogin": message.ownerLogin,
            "ownerCompanyName": _get_company_name(message.ownerLogin),
            "visibility": message.visibility,
            "url": url
        }
    return ans


def send_message(
        first_user_login: str,
        chat_id: int,
        text: str,
        files):
    """Отправляет сообщение пользователю"""
    date = str(datetime.now())[:19]
    if len(Chat.objects.filter(firstUserLogin=first_user_login,
                               id=chat_id)) == 1 or \
            len(Chat.objects.filter(secondUserLogin=first_user_login,
                                    id=chat_id)) == 1:
        if files:
            fileData = files['fileData']
            message = Message(text=text,
                              date=date,
                              chatId=chat_id,
                              ownerLogin=first_user_login,
                              data=fileData)
            message.save()
            print("+++", message.data.url)
            update_files()
            return {"result": True,
                    "text": text,
                    "date": date}
        else:
            message = Message(text=text,
                              date=date,
                              chatId=chat_id,
                              ownerLogin=first_user_login)
            message.save()
            return {"result": True,
                    "text": text,
                    "date": date}
    else:
        return {"result": dictStatus.get(131)}



def get_user(login: str):
    """Получение данных пользователя по логину. Есть обработка секретных полей"""
    if len(User.objects.filter(login=login)) == 1:
        arrExcept = ["_state", "password",
                     "emailRecoveryToken", "token"]
        user = vars(User.objects.get(login=login))
        for item in arrExcept:
            user[item] = 0
        return {"result": True,
                "user": user}
    else:
        return {"result": dictStatus.get(121)}



def check_completeness(login: str):
    """Проверяет заполненность данных пользователя есть массив полей для проверки"""
    if len(User.objects.filter(login=login)) == 1:
        arrExcept = ["country", "companySite",
                     "mainCity", "companyName",
                     "legalAddress", "phone"]
        user = vars(User.objects.get(login=login))
        flag = 1
        incomplete = []
        for item in arrExcept:
            if user[item] == "" or \
                    user[item] == 0 or \
                    user[item] is None:
                flag = 0
                incomplete.append(item)
        return {"result": True,
                "completeness": flag,
                "incomplete": incomplete}
    else:
        return {"result": dictStatus.get(132)}



def register_user(login: str, password: str, role: str, data):
    """Регистрирует пользователя в системе по полному набору данных с фильтрацией"""
    if len(User.objects.filter(login=login)) == 0:
        new_user = User(login=login,
                        password=password,
                        userRole=role,
                        token=getToken(login),
                        email=login)
        new_user.save()

        dictFields = ["firstNM", "secondNM", "userRole", "login",
                      "userType", "email", "directorNM", "country",
                      "companySite", "mainCity", "phone", "companyName",
                      "inn", "kpp", "ogrn", "legalAddress", "fullDescription",
                      "urlComm", "urlServ", "urlHubs"]
        if 'fieldsNames' in data.keys():
            fieldsNames = ast.literal_eval(data['fieldsNames'])
            for item in fieldsNames.keys():
                fieldName = item
                if fieldName in dictFields:
                    setattr(new_user, fieldName, fieldsNames[fieldName])
                    new_user.save()
                    print("+++ ", "added field", fieldName)
                else:
                    print("--- ", "not added field", fieldName)
        new_user.save()
        sendRegProofEmail(new_user)
        print(f"New User: {login}")
        return {"name": login,
                "flag": True,
                "result": True,
                "token": getToken(login)}
    else:
        print(f"User in the DB: {data['log']}")
        return {"result": dictStatus.get(101)}


def make_js_dict(user):
    chatList = list(Chat.objects.filter(firstUser=user)) + \
               list(Chat.objects.filter(secondUser=user))

    messageListStr = "["
    firstUserAddress = ""

    for chat in chatList:
        messages = Message.objects.filter(chat=chat)
        for message in messages:
            chatUserName = ""
            if chat.secondUser == user:
                chatUserName = chat.firstUser.username
                firstUserAddress = chatUserName
            else:
                chatUserName = chat.secondUser.username
                firstUserAddress = chatUserName
            res = "['"
            if message.owner == user:
                res += str(message.owner.username + "', '" + chatUserName + "', 0, '")
            else:
                res += str(message.owner.username + "', '" + chatUserName + "', 1, '")
            res += str(message.text + "', '" + message.date.strftime("%B %d, %Y") + "'],")
            messageListStr += res
    return messageListStr, firstUserAddress
