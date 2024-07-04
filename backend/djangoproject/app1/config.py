# @Aleksandr Kristal v0.0.1 || add email
import random
import xlsxwriter


dictStatus = {
    100: {
        "statusText": "User Problems",
        "message": ""
    },
    101: {
        "statusText": "User already exists",
        "message": ""
    },
    102: {
        "statusText": "User auth problems",
        "message": ""
    },
    110: {
        "statusText": "Wrong pass",
        "message": ""
    },
    111: {
        "statusText": "Wrong token",
        "message": ""
    },
    112: {
        "statusText": "Wrong access rules",
        "message": ""
    },
    113: {
        "statusText": "Wrong seller login",
        "message": ""
    },
    120: {
        "statusText": "Wrong user data",
        "message": ""
    },
    121: {
        "statusText": "Wrong user login",
        "message": ""
    },
    122: {
        "statusText": "Wrong user password",
        "message": ""
    },
    130: {
        "statusText": "Wrong chat",
        "message": ""
    },
    131: {
        "statusText": "Wrong chat id and login",
        "message": ""
    },
    132: {
        "statusText": "Chat append error",
        "message": ""
    },
    133: {
        "statusText": "Wrong field name",
        "message": ""
    },
    210: {
        "statusText": "Wrong product",
        "message": ""
    },
    211: {
        "statusText": "Wrong product name and id",
        "message": ""
    },
    220: {
        "statusText": "Wrong product data",
        "message": ""
    },
    221: {
        "statusText": "Wrong product base field",
        "message": ""
    },
    222: {
        "statusText": "Wrong product extra fields",
        "message": ""
    },
    300: {
        "statusText": "Wrong System",
        "message": ""
    },
    310: {
        "statusText": "Wrong Email",
        "message": ""
    },
    311: {
        "statusText": "Wrong Email Adress",
        "message": ""
    },
    312: {
        "statusText": "Don't have user email",
        "message": ""
    },
    313: {
        "statusText": "SMTP server error",
        "message": ""
    },
    400: {
        "statusText": "Wrong site data",
        "message": ""
    },
    410: {
        "statusText": "Wrong site data data",
        "message": ""
    },
    411: {
        "statusText": "Wrong site data name",
        "message": ""
    },
    500: {
        "statusText": "Wrong system",
        "message": ""
    },
    510: {
        "statusText": "Wrong files in system",
        "message": ""
    },
    511: {
        "statusText": "Wrong file name in system",
        "message": ""
    },
    512: {
        "statusText": "Wrong file owner in system",
        "message": ""
    },
}

password_recovery = "Вам отправлено письмо со ссылкой на восстановление пароля. Ссылка пришла с сайта: naletay.shop \n\n" \
                    "Для восстановления пароля перейдите по ссылке:\n\n" \
                    "http://127.0.0.1:8000/user/recovery \n\n" \
                    "Ваш код:\n\n"
proof_email = "Вам отправлено письмо со ссылкой на подтверждение аккаунта. Ссылка пришла с сайта: naletay.shop \n\n" \
                    "Для восстановления пароля перейдите по ссылке:\n\n" \
                    "http://127.0.0.1:8000/user/proof \n\n" \
                    "Ваш код:\n\n"

password_recovery_title = "Восстановление пароля"
proof_email_title = "Подтверждение регистрации"


def getRandomCode(number):
    res_str = ""
    for i in range(number):
        res_str += chr(65 + int(random.random()*57))
    return res_str


def fullString(string, charNumber):
    if len(string) > charNumber:
        return string[:charNumber]
    else:
        return string + ' ' * (charNumber - len(string))

#def crate_file_by_
