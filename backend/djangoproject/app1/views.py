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

from users.models import User, Chat, Message
from users.models import getToken
from products.models import Product, Commodity, Service, DroneHub

from app1.models import Worker, Post, CustomForm, EmailForm, UserFile
from app1.models import News
from app1.models import getToken
from django.http import JsonResponse
from django.core.mail import send_mail
import datetime

from app1.config import \
    password_recovery, \
    password_recovery_title, \
    proof_email_title, \
    proof_email, \
    getRandomCode

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
    get_news


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
    if request.method == 'POST':
        print(request.POST['userLogin'])
        userLogin = request.POST['userLogin']
        token = request.POST['token']
        classToEdit = request.POST['classToEdit']
        if len(User.objects.filter(login=userLogin, token=token)) == 1:
            user = User.objects.get(login=userLogin)
            if classToEdit == "User":
                fieldName = request.POST['fieldName']
                dictFields = ["firstNM", "secondNM", "userRole", "login",
                              "userType", "email", "directorNM", "country",
                              "companySite", "mainCity", "phone", "companyName",
                              "inn", "kpp", "ogrn", "legalAddress", "fullDescription",
                              "urlComm", "urlServ", "urlHubs", "pass"]
                if fieldName in dictFields:
                    return JsonResponse({"result": True,
                                         "login": userLogin,
                                         "fieldName": fieldName,
                                         "value": getattr(user, fieldName)})
                else:
                    return JsonResponse({"result": dictStatus.get(133),
                                         "fieldName": fieldName})
            elif classToEdit == "Product":
                dictFields = ["photoLink", "speed", "description",
                              "userId", "price", "articleNumber",
                              "flightTime", "range", "weight",
                              "maxWind", "maxAltitude", "minAltitude",
                              "motorsNumber"]
                name = request.POST['name']
                fieldName = request.POST['fieldName']
                if (fieldName in dictFields) and \
                        (len(Product.objects.filter(name=name)) == 1):
                    product = Product.objects.get(name=name)
                    return JsonResponse({"result": True,
                                         "login": userLogin,
                                         "fieldName": fieldName,
                                         "value": getattr(product, fieldName)})
                else:
                    return JsonResponse({"result": dictStatus.get(133),
                                         "fieldName": fieldName})
            elif classToEdit == "UserSuperGet":
                dictFields = ["firstNM", "secondNM", "userRole", "login",
                              "userType", "email", "directorNM", "country",
                              "companySite", "mainCity", "phone", "companyName",
                              "inn", "kpp", "ogrn", "legalAddress", "fullDescription",
                              "urlComm", "urlServ", "urlHubs", "password"]
                fieldsNames = ast.literal_eval(request.POST['fieldsNames'])
                for item in fieldsNames.keys():
                    if item in dictFields:
                        fieldsNames[item] = getattr(user, item)
                return JsonResponse({"result": True,
                                     "login": userLogin,
                                     "fieldsNames": fieldsNames})
        else:
            return JsonResponse({"result": dictStatus.get(102)})
    return render(request, 'get/index.html')


@csrf_exempt
def index_set(request):
    if request.method == 'POST':
        userLogin = request.POST['userLogin']
        token = request.POST['token']
        classToEdit = request.POST['classToEdit']
        if len(User.objects.filter(login=userLogin, token=token)) == 1:
            user = User.objects.get(login=userLogin)
            if classToEdit == "User":
                fieldName = request.POST['fieldName']
                newValue = request.POST['newValue']
                dictFields = ["firstNM", "secondNM", "userRole", "login",
                              "userType", "email", "directorNM", "country",
                              "companySite", "mainCity", "phone", "companyName",
                              "inn", "kpp", "ogrn", "legalAddress", "fullDescription",
                              "urlComm", "urlServ", "urlHubs", "password"]
                if fieldName in dictFields:
                    setattr(user, fieldName, newValue)
                    user.save()
                    return JsonResponse({"result": True,
                                         "login": userLogin,
                                         "fieldName": fieldName,
                                         "newValue": newValue})
                else:
                    return JsonResponse({"result": dictStatus.get(221),
                                         "fieldName": fieldName})
            elif classToEdit == "Product":
                fieldName = request.POST['fieldName']
                newValue = request.POST['newValue']
                name = request.POST['name']
                dictFields = ["photoLink", "speed", "description",
                              "userId", "price", "articleNumber",
                              "flightTime", "range", "weight",
                              "maxWind", "maxAltitude", "minAltitude",
                              "motorsNumber"]
                # print(fieldName, user.id)
                if (len(Product.objects.filter(name=name, userId=user.id)) == 1) \
                        and (fieldName in dictFields):
                    product = Product.objects.get(name=name)
                    setattr(product, fieldName, newValue)
                    product.save()
                    return JsonResponse({"result": True,
                                         "login": userLogin,
                                         "fieldName": fieldName,
                                         "newValue": newValue})
                else:
                    return JsonResponse({"result": dictStatus.get(221)})
            elif classToEdit == "UserSuperSet":
                dictFields = ["firstNM", "secondNM", "userRole", "login",
                              "userType", "email", "directorNM", "country",
                              "companySite", "mainCity", "phone", "companyName",
                              "inn", "kpp", "ogrn", "legalAddress", "fullDescription",
                              "urlComm", "urlServ", "urlHubs", "password"]
                fieldsNames = ast.literal_eval(request.POST['fieldsNames'])
                for item in fieldsNames.keys():
                    fieldName = item
                    if fieldName in dictFields:
                        setattr(user, fieldName, fieldsNames[fieldName])
                        user.save()
                        print("+++ ", "added field", fieldName)
                    else:
                        print("--- ", "not added field", fieldName)
                return JsonResponse({"result": True,
                                     "login": userLogin})
        else:
            return JsonResponse({"result": dictStatus.get(102)})
    return render(request, 'set/index.html')


@csrf_exempt
def index_checkSettings(request):
    if request.method == 'POST':
        userLogin = request.POST['userLogin']
        whatToCheck = request.POST['whatToCheck']
        if len(User.objects.filter(login=userLogin)) == 1:
            if whatToCheck == "token":
                token = request.POST['token']
                if len(User.objects.filter(login=userLogin,
                                           token=token)) == 1:
                    return JsonResponse({"result": True,
                                         "login": userLogin})
                else:
                    return JsonResponse({"result": dictStatus.get(102),
                                         "login": userLogin})
        else:
            return JsonResponse({"result": dictStatus.get(102)})
    return render(request, 'checkSettings/index.html')


@csrf_exempt
def upload_photo(request):
    if request.method == 'POST' and request.FILES:
        typeAction = request.POST['typeAction']
        if typeAction == "addPost":
            text = request.POST['text']
            filePhoto = request.FILES['filePhoto']
            fileData = request.FILES['fileData']

            post = Post(title=text,
                        cover=filePhoto,
                        fileData=fileData)
            post.save()

            return render(request,
                          'upload_file/index.html')
        elif typeAction == "addFile":
            login = request.POST['login']
            fileData = request.FILES['fileData']
            token = request.POST['token']
            typeProduct = request.POST['typeProduct']
            print("========================================", typeProduct)
            print("++", login, token)
            user = User.objects.get(login=login, token=token)

            if len(User.objects.filter(login=login, token=token)) == 1:
                if typeProduct == "commodity":
                    user.fileData = fileData
                    url = os.getenv('DJANGO_BACKEND_URL', 'http://127.0.0.1:8000') + \
                          "/static" + \
                          str(user.fileData.url)[6:]
                    user.urlComm = url
                    user.save()

                    print(user.fileData.url[1:])
                    curDF = pd.read_excel(user.fileData.url[1:])
                    Commodity.objects.filter(userLogin=user.login).update(visibility=0)
                    Product.objects.filter(userLogin=user.login,
                                           type="commodity").delete()
                    print(111)
                    for i in range(len(curDF.values)):
                        print(i)
                        print(len(curDF.values[i]))
                        settings, first, second, third = returnDict(curDF.values[i])

                        print("====================", returnDict(curDF.values[i]))

                        commodity = Commodity(
                            userLogin=user.login,
                            article=settings["article"],
                            manufacturer=settings["manufacturer"],
                            manufacturersCountry=settings["manufacturersCountry"],
                            productName=settings["productName"],
                            price=0,
                            unitMeasurement=settings["unitMeasurement"],
                            productDescription=settings["productDescription"],
                            link1=settings["link1"],
                            link2=settings["link2"],
                            link3=settings["link3"],
                            link4=settings["link4"],
                            link5=settings["link5"],
                            minQuantityToOrder=settings["minQuantityToOrder"],
                            category=settings["category"],
                            maxRangePayload=first["maxRangePayload"],
                            maxTakeoffWeight=first["maxTakeoffWeight"],
                            maxFlightSpeed=first["maxFlightSpeed"],
                            maxDuration=first["maxDuration"],
                            numberOfEngines=second["numberOfEngines"],
                            engineType=second["engineType"],
                            engineCapacity=second["engineCapacity"],
                            takeoffMethod=second["takeoffMethod"],
                            rangeCommunicationLine=second["rangeCommunicationLine"],
                            maxFlightAltitude=second["maxFlightAltitude"],
                            cruisingFlightSpeed=second["cruisingFlightSpeed"],
                            minCrew=second["minCrew"],
                            operatingTemperatureRangeAir=second["operatingTemperatureRangeAir"],
                            maxPermissibleWindSpeed=second["maxPermissibleWindSpeed"],
                            overallCharacteristicsUAV=second["overallCharacteristicsUAV"],
                            typicalPayload=second["typicalPayload"],
                            standardWarranty=second["standardWarranty"],
                            mainPurposes=second["mainPurposes"],
                            mainBranches=second["mainBranches"],
                            extrasForModel=second["extrasForModel"],
                            specification=second["specification"],
                            specificationFile=second["specificationFile"],
                            frequencyCommunication=third["frequencyCommunication"],
                            maxLengthRoute=third["maxLengthRoute"],
                            dimensionsTransportedCargo=third["dimensionsTransportedCargo"],
                            abilityFlyThunderstorms=third["abilityFlyThunderstorms"],
                            possibilityFlyingIcyConditions=third["possibilityFlyingIcyConditions"],
                            overallCharacteristicsTransportCondition=third["overallCharacteristicsTransportCondition"],
                            option1=third["option1"],
                            option2=third["option2"],
                            option3=third["option3"],
                            compositionSupplyPackage=third["compositionSupplyPackage"],
                            preinstalledSoftware=third["preinstalledSoftware"],
                            additionallySuppliedSoftware=third["additionallySuppliedSoftware"],
                            dateCommencement=third["dateCommencement"],
                            productCompliance=third["productCompliance"],
                            statusReceiving=third["statusReceiving"],
                            supplierLicense=third["supplierLicense"],
                            supplierAccreditation=third["supplierAccreditation"],
                            visibility=third["visibility"])
                        commodity.save()

                        product = Product(
                            userLogin=user.login,
                            name=commodity.productName,
                            price=commodity.price,
                            description=commodity.productDescription,
                            type="commodity",
                            characteristicsID=commodity.id
                        )
                        product.save()
                elif typeProduct == "service":
                    user.fileService = fileData
                    url = os.getenv('DJANGO_BACKEND_URL', 'http://127.0.0.1:8000') + "/static" + \
                          str(user.fileService.url)[6:]
                    user.urlServ = url
                    user.save()

                    print("==", str(user.fileService.url)[1:])
                    curDF = pd.read_excel(str(user.fileService.url)[1:])
                    print(curDF)
                    Service.objects.filter(userLogin=user.login).update(visibility=0)
                    Product.objects.filter(userLogin=user.login,
                                           type="service").delete()

                    for i in range(len(curDF.values)):
                        settings = returnService(curDF.values[i])

                        print("++++", settings)
                        service = Service(
                            userLogin=user.login,
                            article=settings["article"],
                            productName=settings["productName"],
                            category=settings["category"],
                            description=settings["description"],
                            applicationScenario=settings["applicationScenario"],
                            # segmentsOfIndustry=settings["segmentsOfIndustry"],
                            link1=settings["link1"],
                            link2=settings["link2"],
                            link3=settings["link3"],
                            specification=settings["specification"],
                            visibility=1)
                        service.save()
                        product = Product(
                            userLogin=user.login,
                            name=service.productName,
                            price=0,
                            description=service.description,
                            type=typeProduct,
                            characteristicsID=service.id)
                        product.save()
                        print(service, product)
                elif typeProduct == "droneHub":
                    user.fileDroneHub = fileData
                    url = os.getenv('DJANGO_BACKEND_URL', 'http://127.0.0.1:8000') + \
                          "/static" + \
                          str(user.fileDroneHub.url)[6:]
                    user.urlHubs = url
                    user.save()

                    curDF = pd.read_excel(str(user.fileDroneHub.url)[1:])
                    DroneHub.objects.filter(userLogin=user.login).update(visibility=0)
                    Product.objects.filter(userLogin=user.login,
                                           type="droneHub").delete()

                    for i in range(len(curDF.values)):
                        print(i)
                        print(len(curDF.values[i]))
                        settings, first, second, third = returnDict(curDF.values[i])
                        droneHub = DroneHub(
                            userLogin=user.login,
                            article=settings["article"],
                            manufacturer=settings["manufacturer"],
                            manufacturersCountry=settings["manufacturersCountry"],
                            productName=settings["productName"],
                            price=settings["price"],
                            unitMeasurement=settings["unitMeasurement"],
                            productDescription=settings["productDescription"],
                            link1=settings["link1"],
                            link2=settings["link2"],
                            link3=settings["link3"],
                            link4=settings["link4"],
                            link5=settings["link5"],
                            minQuantityToOrder=settings["minQuantityToOrder"],
                            category=settings["category"],
                            maxRangePayload=first["maxRangePayload"],
                            maxTakeoffWeight=first["maxTakeoffWeight"],
                            maxFlightSpeed=first["maxFlightSpeed"],
                            maxDuration=first["maxDuration"],
                            numberOfEngines=second["numberOfEngines"],
                            engineType=second["engineType"],
                            engineCapacity=second["engineCapacity"],
                            takeoffMethod=second["takeoffMethod"],
                            rangeCommunicationLine=second["rangeCommunicationLine"],
                            maxFlightAltitude=second["maxFlightAltitude"],
                            cruisingFlightSpeed=second["cruisingFlightSpeed"],
                            minCrew=second["minCrew"],
                            operatingTemperatureRangeAir=second["operatingTemperatureRangeAir"],
                            maxPermissibleWindSpeed=second["maxPermissibleWindSpeed"],
                            overallCharacteristicsUAV=second["overallCharacteristicsUAV"],
                            typicalPayload=second["typicalPayload"],
                            standardWarranty=second["standardWarranty"],
                            mainPurposes=second["mainPurposes"],
                            mainBranches=second["mainBranches"],
                            extrasForModel=second["extrasForModel"],
                            specification=second["specification"],
                            specificationFile=second["specificationFile"],
                            frequencyCommunication=third["frequencyCommunication"],
                            maxLengthRoute=third["maxLengthRoute"],
                            dimensionsTransportedCargo=third["dimensionsTransportedCargo"],
                            abilityFlyThunderstorms=third["abilityFlyThunderstorms"],
                            possibilityFlyingIcyConditions=third["possibilityFlyingIcyConditions"],
                            overallCharacteristicsTransportCondition=third["overallCharacteristicsTransportCondition"],
                            option1=third["option1"],
                            option2=third["option2"],
                            option3=third["option3"],
                            compositionSupplyPackage=third["compositionSupplyPackage"],
                            preinstalledSoftware=third["preinstalledSoftware"],
                            additionallySuppliedSoftware=third["additionallySuppliedSoftware"],
                            dateCommencement=third["dateCommencement"],
                            productCompliance=third["productCompliance"],
                            statusReceiving=third["statusReceiving"],
                            supplierLicense=third["supplierLicense"],
                            supplierAccreditation=third["supplierAccreditation"],
                            visibility=third["visibility"])
                        droneHub.save()

                        product = Product(
                            userLogin=user.login,
                            name=droneHub.productName,
                            price=droneHub.price,
                            description=droneHub.productDescription,
                            type=typeProduct,
                            characteristicsID=droneHub.id
                        )
                        product.save()
                else:
                    return JsonResponse({"result": dictStatus.get(221)})
                user.save()
                return render(request,
                              'upload_file/index.html')
            else:
                return JsonResponse({"result": dictStatus.get(102)})
    return render(request,
                  'upload_file/index.html')


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        action = request.POST['action']
        if action == "addOneFile":
            return JsonResponse(upload_single_file(request.POST, request.FILES))
        elif action == "addMultyFiles":
            return JsonResponse(upload_multy_file(request.POST, request.FILES))
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
