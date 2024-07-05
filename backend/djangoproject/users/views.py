# @Aleksandr Kristal v0.0.4 || get user
import ast
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth, messages
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from app1.config import urlAdress, urlAddressGlobal
from users.models import Chat, Message, getToken, IpData, TgUser
from django.contrib.auth.models import User
from app1.views import \
    sendEmail, \
    sendEmailRecovery, \
    sendRegProofEmail
from app1.config import \
    password_recovery, \
    password_recovery_title, \
    getRandomCode, \
    dictStatus
import os
from users.services import \
    get_user_token, \
    update_files, \
    send_recovery_link, \
    get_recovery_link, \
    send_email, \
    create_chat, \
    get_chats, \
    get_chat_messages, \
    send_message, \
    get_user, \
    check_completeness,\
    register_user, \
    get_all_sellers, \
    read_message, \
    read_chat
from users.forms import \
    UserLoginForm, \
    UserRegistrationForm, \
    UserProfileForm, \
    UserAddChatForm
from orders.models import Basket


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


@csrf_exempt
def index_form(request):
    if request.method == 'POST':
        login = request.POST.get('user', '_')
        password = request.POST.get('pass', '_')
        return JsonResponse(get_user_token(login, password))
    return render(request, 'form/index.html')


@csrf_exempt
def index_get_partners(request):
    if request.method == 'POST':
        actionType = request.POST.get('actionType', '_')
        if actionType == "getAllSellers":
            seller_list = get_all_sellers()
            return JsonResponse(seller_list)
    return render(request, 'get/index_get_sellers.html')


@csrf_exempt
def index_recovery(request):
    if request.method == 'POST':
        actionType = request.POST.get('actionType', '_')
        if actionType == 'sendRecoveryLink':
            login = request.POST.get('user', '')
            return JsonResponse(send_recovery_link(
                login))
        elif actionType == 'getRecoveryLink':
            token = request.POST.get('token', '')
            pass1 = request.POST.get('pass1', '')
            pass2 = request.POST.get('pass2', '')
            return JsonResponse(get_recovery_link(
                token,
                pass1,
                pass2))
    return render(request, 'form/index_recovery.html')


@csrf_exempt
def index_send_email(request):
    if request.method == 'POST':
        actionType = request.POST['actionType']
        if actionType == 'sendEmail':
            title = request.POST.get('title', '')
            text = request.POST.get('text', '')
            email = request.POST.get('email', '')
            return JsonResponse(send_email(
                title,
                text,
                email))
    return render(request, 'form/index_send_email.html')


@ip_save
@login_required
def index_chat(request):
    if request.method == 'POST':
        form = UserAddChatForm(data=request.POST)
        if 'second_user_login' in request.POST.keys():
            print(request.POST)
            second_user_login = request.POST['second_user_login']
            filterSecond = User.objects.filter(username=second_user_login)
            title = ''
            if 'title' in request.POST.keys():
                title = request.POST['title']
            print()
            if len(filterSecond) == 1 and \
                    len(Chat.objects.filter(firstUserLogin=second_user_login,
                                            title=title)) == 0 and \
                    len(Chat.objects.filter(secondUserLogin=second_user_login,
                                            title=title)) == 0:
                secondUser = User.objects.get(username=second_user_login)
                newChat = Chat(firstUser=request.user,
                               secondUser=secondUser,
                               title=title,
                               visibility=1)
                newChat.save()
    chatList = list(Chat.objects.filter(firstUser=request.user)) + \
               list(Chat.objects.filter(secondUser=request.user))

    messageListStr = "["
    firstUserAddress = ""

    for chat in chatList:
        messages = Message.objects.filter(chat=chat)
        for message in messages:
            chatUserName = ""
            if chat.secondUser == request.user:
                chatUserName = chat.firstUser.username
                firstUserAddress = chatUserName
            else:
                chatUserName = chat.secondUser.username
                firstUserAddress = chatUserName
            res = "['"
            if message.owner == request.user:
                res += str(message.owner.username + "', '" + chatUserName + "', 0, '")
            else:
                res += str(message.owner.username + "', '" + chatUserName + "', 1, '")
            res += str(message.text + "', '" + message.date.strftime("%B %d, %Y") + "'],")
            messageListStr += res

    print("messageList ", messageListStr)
    print("+-+-===", urlAdress)
    context = {'form': UserAddChatForm(),
               'chatList': chatList,
               'messageList': messageListStr + "]",
               'currentUserName': request.user.username,
               'firstUserAddress': firstUserAddress,
               'urlAdress': urlAddressGlobal,
               'chat_js_include': 1}
    print(context)
    return render(
        request,
        'users/chat.html',
        context)


@csrf_exempt
def index_get(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == "GetUser":
            login = request.POST['login']
            return JsonResponse(get_user(login))
    return render(request, 'get/index_user.html')


@csrf_exempt
def index_get_completeness(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == "CheckCompleteness":
            login = request.POST['login']
            return JsonResponse(check_completeness(login))
    return render(request, 'get/index_completeness.html')


@csrf_exempt
def index_register(request):
    if request.method == 'POST':
        login = request.POST['log']
        password = request.POST['pass']
        role = request.POST['role']
        data = request.POST
        return JsonResponse(register_user(login, password, role, data))
    return render(request, 'register/index.html')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            userName = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=userName,
                                     password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()
    context = {'form': UserLoginForm()}
    return render(request, 'users/login.html', context)





@csrf_exempt
def registration(request):
    return render(request)


@ip_save
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user,
                               data=request.POST,
                               files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    # baskets = Basket.objects.filter(user=request.user)

    context = {'form': form,
               # 'baskets': baskets,
               'baskets': Basket.objects.all(),
               'volume': 123,#request.user.walletVolume / 10 ** 6,
               'address': "jksdlknsaldvknadksv"#request.user.walletAddress
               }
    return render(request,
                  'users/profile.html',
                  context)


@csrf_exempt
@ip_save
def index_wallet(request):
    return render(request)


@ip_save
def logout(request):
    return HttpResponseRedirect('/')


@ip_save
@login_required
def chat(request):
    return render(request, 'users/chat.html')


@ip_save
@login_required
def addMessage(request, chatAddress, value):
    # http://46.138.245.249:5070/user/addMessage/st2257/a!!!!ascasc/
    user_addressee = User.objects.get(username=chatAddress)
    print("---------------------------------------------", chatAddress)
    print("---------------------------------------------", request.user.username)
    print("---------------------------------------------", len(Chat.objects.filter(firstUser=user_addressee,
                                                                                   secondUser=request.user)))
    if len(Chat.objects.filter(firstUser=user_addressee,
                               secondUser=request.user)) == 1:
        chat = Chat.objects.get(firstUser=user_addressee,
                                secondUser=request.user)
        messages = Message(chat=chat,
                           owner=request.user,
                           text=value)
        messages.save()
    elif len(Chat.objects.filter(secondUser=user_addressee,
                                 firstUser=request.user)) == 1:
        chat = Chat.objects.get(secondUser=user_addressee,
                                firstUser=request.user)
        messages = Message(chat=chat,
                           owner=request.user,
                           text=value)
        messages.save()
    return HttpResponseRedirect('/')


@csrf_exempt
@ip_save
def index_wallet(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user,
                               data=request.POST,
                               files=request.FILES)

        if "typeAction" in request.POST.keys():
            if request.POST["typeAction"] == "sendMoney":
                walletAddress = request.POST["walletAddress"]
                amount = float(request.POST["amount"])
                print(walletAddress, amount)
                if request.user.walletVolume > 10 ** 6 * 0.9 * amount \
                        and amount > 0.001:
                    print(str(amount), amount)
                elif amount <= 0.001:
                    print("To small amount")
                else:
                    print("Error: not enouth TON for send")
    else:
        form = UserProfileForm(instance=request.user)

    request.user.data.walletVolume = int(float(9876543) * 1000000)
    request.user.data.walletAddress = "skbvskdbvkb3k2j3bj34k234fjb2b2kdvvd"
    request.user.data.save()
    context = {'form': form,
               'volume': request.user.data.walletVolume / 10 ** 6,
               'address': request.user.data.walletAddress
               }
    return render(request,
                  'users/wallet.html',
                  context)
