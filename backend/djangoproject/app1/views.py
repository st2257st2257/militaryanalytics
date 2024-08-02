# @Aleksandr Kristal v0.1.0 || add email
import os
from openpyxl import load_workbook
import urllib
from io import BytesIO
import pandas as pd
import ast
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import xlrd, xlwt
from orders.models import SubDivType, OrderType, Order, Basket
from users.models import Chat, Message
"""User"""
from users.models import getToken
from django.contrib.auth.models import User
from app1.models import Worker, Post, CustomForm, EmailForm, UserFile
from app1.models import News
from app1.models import getToken
from django.http import JsonResponse
from django.core.mail import send_mail
import datetime

from kafka import KafkaConsumer, KafkaProducer

import json
import time

from app1.config import \
    password_recovery, \
    password_recovery_title, \
    proof_email_title, \
    proof_email, \
    getRandomCode, \
    full_rus_uk_text, full_is_hum_text

from app1.config import \
    dictStatus

from djangoproject.settings import EMAIL_HOST_USER

from app1.services import \
    send_email_recovery, \
    send_email, \
    send_reg_proof_email, \
    returnDict, \
    returnService, \
    upload_single_file, \
    upload_multy_file, \
    get_file_by_name, \
    get_file_by_type, \
    get_file_by_class, \
    get_news, \
    create_user, \
    create_super_user, \
    create_sub_div_type, \
    create_order_type


def sendEmailRecovery(title, text, address, code):
    sendEmail(title, text + code, address)


def sendEmail(title, text, address):
    send_mail(
        title,
        text,
        EMAIL_HOST_USER,
        [address],
        fail_silently=False,
    )


def sendRegProofEmail(user):
    title = proof_email_title
    text = proof_email + getRandomCode(9)
    send_email(title, text, user.email)


@csrf_exempt
def index_kafka_send(request):
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092"
    )

    topic = "light_new"
    producer.send(topic, 'Hello Kafka World1234!')

    print(f"Published message to {topic}")
    return JsonResponse({"result": True})


@csrf_exempt
def index_make_default(request):
    res = {}

    # Create default user
    res["Admin login"] = create_super_user("supadmin", "wacze000", "kristal.as@phystech.edu")

    # Create base users
    res["user1"] = create_user("user1", "pass1", "user1@militarybet.com")
    res["user2"] = create_user("user2", "pass2", "user2@militarybet.com")
    res["user3"] = create_user("user3", "pass3", "user3@militarybet.com")
    res["support"] = create_user("support", "pass_sup", "support@militarybet.com")

    # Create sub div type
    res["uk_rus"] = create_sub_div_type(
        "Russian-Ukrain conflict",
        "Conflict in the middle of west Europe",
        full_rus_uk_text)

    res["is_hum"] = create_sub_div_type(
        "Israel–Hamas war",
        "Conflict in the middle East",
        full_is_hum_text)

    # Create Order Type
    uk_rus = SubDivType.objects.get(id=1)
    res["Ukraine lose"] = create_order_type(
        sub_div_type=uk_rus,
        short_name="Ukraine lose",
        short_text=uk_rus.shortText,
        full_text=uk_rus.fullText,
        price=1000)
    res["Russia win"] = create_order_type(
        sub_div_type=uk_rus,
        short_name="Russia win",
        short_text=uk_rus.shortText,
        full_text=uk_rus.fullText,
        price=2000)

    return JsonResponse(res)


@csrf_exempt
def index_page(request):
    #  new_worker = Worker(firstNM='Sidor', secondNM='Fedorovich', salary=300)
    #  new_worker.save()

    # worker_to_change = Worker.objects.get(id=5)
    # worker_to_change.secondNM = 'NewSecondName'
    # worker_to_change.save()
    # print(worker_to_change)

    all_workers = Worker.objects.all()
    filter_workers = Worker.objects.filter(salary=123)

    print("All: ", all_workers)
    print("Filter: ", filter_workers)
    
    # Create default user
    # user = User.objects.create_superuser(
    #     email="kristal.as@phystech.edu",
    #     password="wacze000",
    #     username="supadmin",
    # )
    # user.is_admin = True
    # user.is_staff = True
    # user.save()

    # send_db_mail('welcome-notification', "kristal.as@phystech.edu", {"data": 5})
    # send_email(password_recovery_title,
    #           password_recovery,
    #           "kristal.as@phystech.edu")

    workArr = []
    for item in all_workers:
        print(f'ID: {item.id}  '
              f'Фамилия: {item.firstNM} '
              f'Имя: {item.secondNM} '
              f'ЗП:{item.salary}')
        workArr.append([item.id, item.firstNM, item.secondNM, item.salary])

    return render(request, 'index.html', {'data': 5, 'dataArr': workArr})


@csrf_exempt
def index_news(request):
    if request.method == 'POST':
        if request.POST['type'] == "add":
            news = News(name=request.POST['name'],
                        photoLink=request.POST['photoLink'],
                        description=request.POST['description'],
                        date=str(datetime.datetime.now())[:19],  # request.POST['date']
                        type=int(request.POST['newsType']),
                        userId=int(request.POST['userid']))
            news.save()
            return JsonResponse({"result": True,
                                 "newsName": news.name,
                                 "date": news.date})
        elif request.POST['type'] == "get":
            newsId = -1
            if request.POST['newsId'] != "":
                newsId = int(request.POST['newsId'])
            newsName = request.POST['name']
            if News.objects.filter(id=newsId):
                newsObject = News.objects.get(id=newsId)
                newsObject.save()
                return JsonResponse({"result": True,
                                     "name": newsObject.name,
                                     "photoLink": newsObject.photoLink,
                                     "date": newsObject.date,
                                     "type": newsObject.type,
                                     "userId": newsObject.userId})
            else:
                newsObject = News.objects.get(name=newsName)
                newsObject.save()
                return JsonResponse({"result": True,
                                     "name": newsObject.name,
                                     "photoLink": newsObject.photoLink,
                                     "date": newsObject.date,
                                     "type": newsObject.type,
                                     "userId": newsObject.userId})
        elif request.POST['type'] == "all":
            return JsonResponse({"result": True,
                                 "news_data": get_news()})
    return render(request, 'news/index.html')


@csrf_exempt
def form_add(request, title, data):
    customForm = CustomForm(title=title,
                            data=data)
    customForm.save()
    return JsonResponse({"result": True,
                         "title": title,
                         "data": data})


@csrf_exempt
def form_email(request, title, name, email, phone, company, message):
    fileForm = EmailForm(title=title,
                         name=name,
                         email=email,
                         phone=phone,
                         company=company,
                         message=message)
    # send_mail(
    #     title,
    #     message,
    #     EMAIL_HOST_USER,
    #     [email],
    #     fail_silently=False,
    # )
    fileForm.save()
    return JsonResponse({"result": True,
                         "title": title})


@csrf_exempt
def index_get(request):
    return render(request, 'get/index.html')


@csrf_exempt
def index_set(request):
    return render(request, 'set/index.html')


@csrf_exempt
def index_checkSettings(request):
    return render(request, 'checkSettings/index.html')


@csrf_exempt
def upload_photo(request):
    return render(request,
                  'upload_file/index.html')


@csrf_exempt
def upload_file(request):
    return render(request,
                  'upload_file/index_user.html')


@csrf_exempt
def get_file(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == "getFileName":
            name = request.POST['fileName']
            owner_login = request.POST['userOwner']
            return JsonResponse(get_file_by_name(name, owner_login))
        elif action == "getFileType":
            object_type = request.POST['objectType']
            owner_login = request.POST['userOwner']
            return JsonResponse(get_file_by_type(object_type, owner_login))
        elif action == "getFileClass":
            class_name = request.POST['className']
            owner_login = request.POST['userOwner']
            return JsonResponse(get_file_by_class(class_name, owner_login))
    return render(request,
                  'upload_file/index_file_get.html')
