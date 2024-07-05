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
    return {"result": True}


def update_files():
    src = 'media/messages'
    trg = 'static/messages'
    files = os.listdir(src)
    for fileName in files:
        shutil.copy2(os.path.join(src, fileName), trg)


def get_all_sellers():
    return {"result": True}


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

def get_recovery_link():
    return {"result": True}


def send_email():
    return {"result": True}


def create_chat():
    """Создание чата"""
    return {"result": True}


def get_not_read():
    return {"result": True}


def read_message():
    return {"result": True}


def read_chat():
    return {"result": True}


def get_chats():
    """Получение чатов пользователя"""
    return {"result": True}


def get_chat_messages():
    """Получение сообщений конкретного чата"""
    return {"result": True}


def send_message():
    """Отправляет сообщение пользователю"""
    return {"result": True}


def get_user():
    """Получение данных пользователя по логину. Есть обработка секретных полей"""
    return {"result": True}



def check_completeness():
    """Проверяет заполненность данных пользователя есть массив полей для проверки"""
    return {"result": True}


def register_user():
    """Регистрирует пользователя в системе по полному набору данных с фильтрацией"""
    return {"result": True}


def make_js_dict():
    return {"result": True}
