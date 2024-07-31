import shutil
import os

from django.core.mail import send_mail

from app1.config import \
    password_recovery, \
    password_recovery_title, \
    proof_email_title, \
    proof_email, \
    getRandomCode
from app1.models import News
from users.models import Chat, Message, User

from app1.models import Worker, Post, CustomForm, EmailForm, UserFile
from orders.models import SubDivType, OrderType, Order, Basket

from app1.config import \
    dictStatus

from djangoproject.settings import EMAIL_HOST_USER


def send_email_recovery(title, text, address, code):
    send_email(title, text + code, address)


def send_email(title, text, address):
    send_mail(
        title,
        text,
        EMAIL_HOST_USER,
        [address],
        fail_silently=False,
    )


def create_order_type(sub_div_type, short_name, short_text, full_text, price):
    flag_superuser = len(OrderType.objects.filter(shortName=short_name))
    if flag_superuser == 0:
        order_type = OrderType.objects.create(
            subDivType=sub_div_type,
            shortName=short_name,
            shortText=short_text,
            fullText=full_text,
            averagePrice=price
        )
        order_type.save()
        return "Done"
    else:
        return "Exists"


def create_super_user(username, password, email=""):
    flag_superuser = len(User.objects.filter(username=username))
    if flag_superuser == 0:
        user = User.objects.create_superuser(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save()
        return "Done"
    else:
        return "Exists"


def create_user(username, password, email=""):
    flag_superuser = len(User.objects.filter(username=username))
    if flag_superuser == 0:
        user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.save()
        return "Done"
    else:
        return "Exists"


def create_sub_div_type(short_name, short_text, full_text=""):
    flag_superuser = len(SubDivType.objects.filter(shortName=short_name))
    if flag_superuser == 0:
        sub_div = SubDivType.objects.create(
            shortName=short_name,
            shortText=short_text,
            fullText=full_text,
        )
        sub_div.save()
        return "Done"
    else:
        return "Exists"


def send_reg_proof_email(user):
    title = proof_email_title
    text = proof_email + getRandomCode(9)
    send_email(title, text, user.email)


def returnDict(arrayLine):
    df = arrayLine
    firstIndex = 0
    settings = {"userLogin": -1,
                "article": df[0 + firstIndex],
                "manufacturer": df[1 + firstIndex],
                "manufacturersCountry": df[2 + firstIndex],
                "productName": df[3 + firstIndex],
                "subCategory": df[4 + firstIndex],
                "productType": "commodity",
                "price": df[5 + firstIndex],
                "unitMeasurement": df[6 + firstIndex],
                "productDescription": df[7 + firstIndex],
                "link1": df[8 + firstIndex],
                "link2": df[9 + firstIndex],
                "link3": df[10 + firstIndex],
                "link4": df[11 + firstIndex],
                "link5": df[12 + firstIndex],
                "minQuantityToOrder": df[47 + firstIndex],
                "category": df[48 + firstIndex]}

    first = {"maxRangePayload": df[19 + firstIndex],
             "maxTakeoffWeight": df[21 + firstIndex],
             "maxFlightSpeed": df[24 + firstIndex],
             "maxDuration": df[25 + firstIndex]}

    second = {"numberOfEngines": df[13 + firstIndex],
              "engineType": df[14 + firstIndex],
              "engineCapacity": df[15 + firstIndex],
              "takeoffMethod": df[16 + firstIndex],
              "rangeCommunicationLine": df[17 + firstIndex],
              "maxFlightAltitude": df[22 + firstIndex],
              "cruisingFlightSpeed": df[23 + firstIndex],
              "minCrew": df[26 + firstIndex],
              "operatingTemperatureRangeAir": df[28 + firstIndex],
              "maxPermissibleWindSpeed": df[29 + firstIndex],
              "overallCharacteristicsUAV": df[32 + firstIndex],
              "typicalPayload": df[34 + firstIndex],
              "standardWarranty": df[41 + firstIndex],
              "mainPurposes": df[49 + firstIndex],
              "mainBranches": df[50 + firstIndex],
              "extrasForModel": df[51 + firstIndex],
              "specification": df[51 + firstIndex],
              "specificationFile": df[52 + firstIndex]}
    print("====", df[52 + firstIndex])

    third = {"frequencyCommunication": df[18 + firstIndex],
             "maxLengthRoute": df[20 + firstIndex],
             "dimensionsTransportedCargo": df[27 + firstIndex],
             "abilityFlyThunderstorms": df[30 + firstIndex],
             "possibilityFlyingIcyConditions": df[31 + firstIndex],
             "overallCharacteristicsTransportCondition": df[33 + firstIndex],
             "option1": df[35 + firstIndex],
             "option2": df[36 + firstIndex],
             "option3": df[37 + firstIndex],
             "compositionSupplyPackage": df[38 + firstIndex],
             "preinstalledSoftware": df[39 + firstIndex],
             "additionallySuppliedSoftware": df[40 + firstIndex],
             "dateCommencement": df[42 + firstIndex],
             "productCompliance": df[43 + firstIndex],
             "statusReceiving": df[44 + firstIndex],
             "supplierLicense": df[45 + firstIndex],
             "supplierAccreditation": df[46 + firstIndex],
             "visibility": 1}
    return settings, first, second, third


def returnService(arrayLine):
    dv = arrayLine
    settings = {"userLogin": dv[0],
                "article": dv[1],
                "productName": dv[2],
                "category": dv[3],
                "description": dv[4],
                "applicationScenario": dv[5],
                "subCategory": dv[6],
                "link1": dv[7],
                "link2": dv[8],
                "link3": dv[9],
                "specification": dv[10],
                "visibility": 1}
    return settings


def _get_url(object_type, user_file):
    url = ""
    if object_type=="img":
        url = os.getenv('DJANGO_BACKEND_URL', 'http://127.0.0.1:8000') + \
                "/media/fileImages" + \
                str(user_file.file_image.url)[6:]
    else:
        url = os.getenv('DJANGO_BACKEND_URL', 'http://127.0.0.1:8000') + \
                "/media/fileImages" + \
                str(user_file.file_data.url)[6:]
    return url


def upload_single_file(text_data, file_data):
    class_name = text_data.get('className', 'User')
    user_owner = text_data.get('userOwner', 'blank_user')
    object_type = text_data.get('objectType', 'file')
    file_name = text_data.get('fileName', 'file')
    token = text_data.get('token', None)
    file_image = file_data.get('filePhoto', None)
    file_data = file_data.get('fileData', None)
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        user_file = UserFile(
            class_name=class_name,
            user_owner=user.login,
            object_type=object_type,
            file_name=file_name,
            file_image=file_image,
            file_data=file_data,
        )
        user_file.file_static_url = _get_url(object_type, user_file)
        user_file.save()
        return {"result": True,
                "file_static_url": user_file.file_static_url,
                "fileId": user_file.id}
    elif len(User.objects.filter(login=user_owner)) == 1:
        user_file = UserFile(
            class_name=class_name,
            user_owner=user_owner,
            object_type=object_type,
            file_name=file_name,
            file_image=file_image,
            file_data=file_data,
            visibility=0
        )
        user_file.file_static_url = _get_url(object_type, user_file)
        user_file.save()
        return {"result": True,
                "description": "wrong token. right login",
                "file_static_url": user_file.file_static_url,
                "fileId": user_file.id}
    else:
        return {"result": dictStatus.get(111)}


def upload_multy_file(text_data, file_data):
    class_name = text_data.get('className', 'User')
    file_name = text_data.get('fileName', 'file')
    token = text_data.get('token', None)
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)

        for file in file_data['fileDataMore']:
            print(file)
            user_file = UserFile(
                class_name=class_name,
                user_owner=user.login,
                object_type="",
                file_name=file_name,
                file_data=file,
            )
            user_file.save()
        return {"result": True,
                "file_static_url": user_file.file_static_url,
                "fileId": user_file.id}
    else:
        return {"result": dictStatus.get(111)}


def get_file_by_name(file_name, owner_login):
    if len(User.objects.filter(login=owner_login)) == 1:
        arrayFile = UserFile.objects.filter(user_owner=owner_login,
                                            file_name=file_name)
        if len(arrayFile) >= 1:
            file = arrayFile[len(arrayFile)-1]
            url = file.file_static_url.replace(
                "media",
                "static" ).replace(
                "http://127.0.0.1:8000/",
                "http://naletay.shop:8083/"
            )
            print(url)
            return {
                "result": True,
                "class_name": file.class_name,
                "user_owner": file.user_owner,
                "object_type": file.object_type,
                "file_name": file.file_name,
                "file_static_url": url,
                "visibility": file.visibility
            }
        else:
            return {"result": dictStatus.get(511)}
    else:
        return {"result": dictStatus.get(121)}


def get_file_by_type(object_type, owner_login):
    if len(User.objects.filter(login=owner_login)) == 1:
        arrayFile = UserFile.objects.filter(user_owner=owner_login,
                                            object_type=object_type)
        if len(arrayFile) >= 1:
            result = {"result": True}

            for file in arrayFile:
                print(file.file_static_url)
                file_dict = {
                    "class_name": file.class_name,
                    "user_owner": file.user_owner,
                    "object_type": file.object_type,
                    "file_name": file.file_name,
                    "file_static_url": file.file_static_url,
                    "visibility": file.visibility
                }
                result[file.id] = file_dict
            return result
        else:
            return {"result": dictStatus.get(511)}
    else:
        return {"result": dictStatus.get(121)}


def get_file_by_class(class_name, owner_login):
    if len(User.objects.filter(login=owner_login)) == 1:
        arrayFile = UserFile.objects.filter(user_owner=owner_login,
                                            class_name=class_name)
        if len(arrayFile) >= 1:
            result = {"result": True}

            for file in arrayFile:
                file_dict = {
                    "class_name": file.class_name,
                    "user_owner": file.user_owner,
                    "object_type": file.object_type,
                    "file_name": file.file_name,
                    "file_static_url": file.file_static_url,
                    "visibility": file.visibility
                }
                result[file.id] = file_dict
            return result
        else:
            return {"result": dictStatus.get(511)}
    else:
        return {"result": dictStatus.get(121)}


def get_news():
    res = {}
    news_objects = News.objects.all()
    for news in news_objects:
        res[news.id] = {
            "name": news.name,
            "photoLink": news.photoLink,
            "description": news.description,
            "date": news.date,
            "type": news.type,
            "userId": news.userId
        }
    return res
