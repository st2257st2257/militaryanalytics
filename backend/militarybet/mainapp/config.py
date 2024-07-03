import socket

deploy = False

notAuth = "Для авторизации в сервисе пройдите авторизацию:\n" \
          "/reg\n" \
          "Telegram: t.me/globalcompas\n" \
          "YouTube: https://www.youtube.com/@GlobalCompas"

isAuth = "Вы авторизованы в сервисе\n" \
         "Если хотите сделать ставку, напишите: /new\n" \
         "Telegram: t.me/globalcompas\n" \
         "YouTube: https://www.youtube.com/@GlobalCompas"

mainMenu = "Вы перенесены в главное меню\n" \
           "Основные команды:\n" \
           "⁉ /start начало общения с ботом\n" \
           "📜 /mainMenu основе меню системы\n" \
           "🛒 /market Магазин\n" \
           "🪪 /account Личные данные\n" \
           "📨 /reg Обновление данных"

host = socket.gethostbyname(socket.gethostname())
urlAdress = "https://" + host + ":50" + str(host)[-2:]
urlAddressGlobal = ""
codeIP = str(host)[-2:]

if int(100) < 10:
    urlAddressGlobal = "https://proreef.ru:8000"
else:
    if deploy:
        urlAddressGlobal = "https://46.138.245.249:50"
    else:
        urlAddressGlobal = "https://192.168.1." + codeIP + ":50" + codeIP

print("Url Global: ", urlAddressGlobal)
urlBase = "https://127.0.0.1:8000"
print("Url Local: ", urlBase)
