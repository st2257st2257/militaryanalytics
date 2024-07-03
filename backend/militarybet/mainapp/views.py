from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from mainapp.models import IpData, TgUser


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def addIp(request, functionNM):
    curIp = get_client_ip(request)
    print("curIp: ", curIp)
    if curIp[:4] != "192.":
        ipData = IpData()
        ipData.initIp(curIp=curIp)
        ipData.userName = request.user
        ipData.functionNM = functionNM
        ipData.save()


def ip_save(func):
    def wrapper(*args, **kwargs):
        print("userIp: ", get_client_ip(args[0]), str(func.__name__))
        addIp(args[0], str(func.__name__))
        result = func(*args, **kwargs)
        return result
    return wrapper


@ip_save
@csrf_exempt
def index_page(request):
    print(request.META)
    context = {'is_promotion': True,
               'title': 'MainTitle'}
    return render(request, 'index.html', {'data': 5})


@ip_save
@csrf_exempt
def index_test(request):
    context = {"sale": "-10%",
               "price1": "135 000",
               "price2": "150 000",
               "title": "Смартфон Apple IPhone"}
    arrContext = []
    for i in range(10):
        res = context
        res['id'] = i
        arrContext.append(res)
    arr = {"name": [context for i in range(50)]}
    return render(request, 'test/index.html', context=arrContext)


@csrf_exempt
def index_tgbot(request):
    if request.method == 'POST':
        userId = int(request.POST['userId'])
        if request.POST['actionType'] == "addNew":
            if len(TgUser.objects.filter(userTgId=userId)) == 0:
                newUser = TgUser(userTgId=userId)
                newUser.save()
            else:
                print("Error with adding new user")
        elif request.POST['actionType'] == "editField":
            if len(TgUser.objects.filter(userTgId=userId)) == 1:
                fieldNM = request.POST['fieldNM']
                curUser = TgUser.objects.get(userTgId=int(request.POST['userId']))
                print(request.POST)
                setattr(curUser, fieldNM, request.POST['value'])
                curUser.save()
            else:
                print("Error with editing userTG field")
        elif request.POST['actionType'] == "getUserData":
            if len(TgUser.objects.filter(userTgId=userId)) == 1:
                user = TgUser.objects.get(userTgId=userId)
                data = {
                    "userTgId": user.userTgId,
                    "firstNM": user.firstNM,
                    "secondNM": user.secondNM,
                    "age": user.age,
                }
                return JsonResponse({"type": "True",
                                     "data": data})
            else:
                return JsonResponse({"type": "False",
                                     "data": {}})
    return render(request, 'test/index.html')
