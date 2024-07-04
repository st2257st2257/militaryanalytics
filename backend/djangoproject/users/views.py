# @Aleksandr Kristal v0.0.4 || get user
import ast
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from products.models import Product, Order, Basket, Commodity, Service, DroneHub

from users.models import User, Chat, Message, getToken
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


@csrf_exempt
def index_chat(request):
    if request.method == 'POST':
        actionType = request.POST['actionType']
        token = request.POST['token']
        flag = len(User.objects.filter(token=token))
        if flag == 1:
            if actionType == "createChat":
                first_user_login = request.POST['firstUserLogin']
                second_user_login = request.POST['secondUserLogin']
                return JsonResponse(create_chat(
                    first_user_login,
                    second_user_login))
            elif actionType == "getChats":
                first_user_login = request.POST['firstUserLogin']
                return JsonResponse(get_chats(
                    first_user_login))
            elif actionType == "getChatMessages":
                chat_id = int(request.POST['chatId'])
                return JsonResponse(get_chat_messages(
                    chat_id))
            elif actionType == "sendMessage":
                first_user_login = request.POST['firstUserLogin']
                chat_id = int(request.POST['chatId'])
                text = request.POST['text']
                return JsonResponse(send_message(
                    first_user_login,
                    chat_id,
                    text,
                    request.FILES))
            elif actionType == "readMessage":
                first_user_login = request.POST['firstUserLogin']
                message_id = int(request.POST['messageId'])
                read_message(
                    first_user_login,
                    message_id)
                return JsonResponse({"result": True})
            elif actionType == "readChat":
                first_user_login = request.POST['firstUserLogin']
                chat_id = int(request.POST['chatId'])
                read_chat(
                    first_user_login,
                    chat_id)
                return JsonResponse({"result": True})
        else:
            return JsonResponse({"result": dictStatus.get(132)})
    return render(request, 'message/index.html')


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
