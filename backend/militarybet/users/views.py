import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from mainapp.config import urlAdress, urlAddressGlobal

from mainapp.views import \
    addIp, ip_save

from users.models import \
    User, \
    Chat, Message
from users.forms import \
    UserLoginForm, \
    UserRegistrationForm, \
    UserProfileForm, \
    UserAddChatForm
from orders.models import Basket


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
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешная регистрация')
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


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
    baskets = Basket.objects.filter(user=request.user)

    context = {'form': form,
               'baskets': Basket.objects.all(),
               'baskets': baskets,
               'volume': request.user.walletVolume / 10 ** 6,
               'address': request.user.walletAddress
               }
    return render(request,
                  'users/profile.html',
                  context)


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
                    req = requests.get("http://127.0.0.1:3000/send_for/" +
                                       walletAddress + "/" + str(amount))
                elif amount <= 0.001:
                    print("To small amount")
                else:
                    print("Error: not enouth TON for send")
                print(str(req.content))
    else:
        form = UserProfileForm(instance=request.user)

    reqBalance = requests.get('http://127.0.0.1:3000/balance')
    requests.get('http://127.0.0.1:3000/', data={'key': 'value'})
    volume = str(reqBalance.content)[2:-1]

    reqAddress = requests.get('http://127.0.0.1:3000/address')
    address = str(reqAddress.content)[2:-1]

    request.user.walletVolume = int(float(volume) * 1000000)
    request.user.walletAddress = address
    request.user.save()
    context = {'form': form,
               'volume': request.user.walletVolume / 10 ** 6,
               'address': request.user.walletAddress
               }
    return render(request,
                  'users/wallet.html',
                  context)


@ip_save
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@ip_save
@login_required
def chat(request):
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
                newChat = Chat(firstUserLogin=request.user.username,
                               secondUserLogin=second_user_login,
                               firstUserName=request.user.first_name,
                               secondUserName=secondUser.first_name,
                               title=title,
                               visibility=1)
                newChat.save()
    chatList = list(Chat.objects.filter(firstUserLogin=request.user.username)) + \
               list(Chat.objects.filter(secondUserLogin=request.user.username))

    messageListStr = "["
    firstUserAddress = ""

    for chat in chatList:
        messages = Message.objects.filter(chatId=chat.id)
        for message in messages:
            chatUserName = ""
            if chat.secondUserLogin == request.user.username:
                chatUserName = chat.firstUserLogin
                firstUserAddress = chatUserName
            else:
                chatUserName = chat.secondUserLogin
                firstUserAddress = chatUserName
            res = "['"
            if message.ownerLogin == request.user.username:
                res += str(message.ownerLogin + "', '" + chatUserName + "', 0, '")
            else:
                res += str(message.ownerLogin + "', '" + chatUserName + "', 1, '")
            res += str(message.text + "', '" + message.date.strftime("%B %d, %Y") + "'],")
            messageListStr += res

    print("messageList ", messageListStr)
    print("+-+-===", urlAdress)
    context = {'form': UserAddChatForm(),
               'chatList': chatList,
               'messageList': messageListStr + "]",
               'currentUserName': request.user.username,
               'firstUserAddress': firstUserAddress,
               'urlAdress': urlAddressGlobal}
    return render(request, 'users/chat.html', context)


@ip_save
@login_required
def addMessage(request, chatAddress, value):
    # http://46.138.245.249:5070/user/addMessage/st2257/a!!!!ascasc/
    print("---------------------------------------------", chatAddress)
    print("---------------------------------------------", request.user.username)
    print("---------------------------------------------", len(Chat.objects.filter(firstUserLogin=chatAddress,
                                                                                   secondUserLogin=request.user.username)))
    if len(Chat.objects.filter(firstUserLogin=chatAddress,
                               secondUserLogin=request.user.username)) == 1:
        chat = Chat.objects.get(firstUserLogin=chatAddress,
                                secondUserLogin=request.user.username)
        messages = Message(chatId=chat.id,
                           ownerLogin=request.user.username,
                           text=value)
        messages.save()
    elif len(Chat.objects.filter(secondUserLogin=chatAddress,
                                 firstUserLogin=request.user.username)) == 1:
        chat = Chat.objects.get(secondUserLogin=chatAddress,
                                firstUserLogin=request.user.username)
        messages = Message(chatId=chat.id,
                           ownerLogin=request.user.username,
                           text=value)
        messages.save()
    return HttpResponseRedirect('/')

