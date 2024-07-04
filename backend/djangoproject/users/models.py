# @Aleksandr Kristal v0.0.2 || add
from datetime import datetime
from django.contrib import admin

from django.db import models
from app1.config import fullString
import datetime


def getToken(login):
    return login + str(datetime.now())[:19]


class IpData(models.Model):
    ip4 = models.CharField(max_length=128, blank=True)
    ip6 = models.CharField(max_length=128, blank=True)
    userName = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    loc = models.CharField(max_length=128, blank=True)
    org = models.CharField(max_length=128, blank=True)
    timezone = models.CharField(max_length=128, blank=True)
    hostname = models.CharField(max_length=128, blank=True)
    functionNM = models.CharField(max_length=128, blank=True)
    # brandMoser = models.CharField(max_length=128, blank=True)
    # isJsOn = models.BooleanField(blank=True)
    language = models.CharField(max_length=128, blank=True)
    date = models.CharField(max_length=128, blank=True)
    data = models.CharField(max_length=128, blank=True)

    def initIp(self, curIp):
        self.getBaseData(curIp)

    def getBaseData(self, curIp):
        endpoint = f'https://ipinfo.io/{curIp}/json'

    def __str__(self):
        return f'{self.ip4} {self.userName} {self.functionNM}'


class TgUser(models.Model):
    userTgId = models.BigIntegerField(default=0)
    firstNM = models.CharField(max_length=128, blank=True)
    secondNM = models.CharField(max_length=128, blank=True)
    age = models.CharField(max_length=128, blank=True)
    rightData = models.CharField(max_length=128, blank=True)


class Access(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'ID: {self.id} | Name: {self.name}'


class User(models.Model):
    accessID = models.IntegerField(default=1)
    login = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=100, blank=False)
    firstNM = models.CharField(max_length=100, blank=True)
    secondNM = models.CharField(max_length=100, blank=True)
    thirdNM = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=40, blank=True)
    userRole = models.CharField(max_length=40, blank=True)
    userType = models.CharField(max_length=40, blank=True)
    fileData = models.FileField(upload_to='fileData/', blank=True)
    urlComm = models.CharField(max_length=100, blank=True)
    fileService = models.FileField(upload_to='fileService/', blank=True)
    urlServ = models.CharField(max_length=100, blank=True)
    fileDroneHub = models.FileField(upload_to='fileDroneHub/', blank=True)
    urlHubs = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    emailRecoveryToken = models.CharField(max_length=100, blank=True)
    directorNM = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    companySite = models.CharField(max_length=100, blank=True)
    mainCity = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    companyName = models.CharField(max_length=100, blank=True)
    inn = models.CharField(max_length=100, blank=True)
    kpp = models.CharField(max_length=100, blank=True)
    ogrn = models.CharField(max_length=100, blank=True)
    legalAddress = models.CharField(max_length=1000, blank=True)
    fullDescription = models.CharField(max_length=100, blank=True)
    # ggz = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'ID:{self.id} | Login: {self.login}'


class Chat(models.Model):
    firstUserLogin = models.CharField(max_length=40, blank=True)
    secondUserLogin = models.CharField(max_length=40, blank=True)
    firstUserName = models.CharField(max_length=40, blank=True)
    secondUserName = models.CharField(max_length=40, blank=True)
    visibility = models.IntegerField(default=0)
    notReadFirst = models.IntegerField(default=0)
    notReadSecond = models.IntegerField(default=0)

    def __str__(self):
        return f'ID: {self.id} | {self.firstUserLogin} <=> {self.secondUserLogin}'


class Message(models.Model):
    text = models.CharField(max_length=1024, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    chatId = models.IntegerField(default=0)
    ownerLogin = models.CharField(max_length=40, blank=True)
    data = models.FileField(upload_to='messages/', blank=True)
    visibility = models.IntegerField(default=1)
    notRead = models.IntegerField(default=1)

    def __str__(self):
        return f'Chat: {self.chatId} | Text: {fullString(self.text, 100)}'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id", "accessID", "login", "userRole", "email", "companyName", )
    list_display = ("id", "accessID", "login", "userRole", "email", "companyName", )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    search_fields = ("id", "firstUserLogin", "secondUserLogin", "firstUserName", "secondUserName", )
    list_display = ("id", "firstUserLogin", "secondUserLogin", "firstUserName", "secondUserName", )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields = ("id", "chatId", "ownerLogin", )
    list_display = ("id", "chatId", "ownerLogin", "text", "date", )
