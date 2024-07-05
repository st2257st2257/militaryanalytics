# @Aleksandr Kristal v0.0.2 || add
from datetime import datetime
from django.contrib import admin

from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


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

    def __str__(self):
        return f'ID: {self.userTgId} | Name: {self.firstNM}'


class Access(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'ID: {self.id} | Name: {self.name}'


class Data(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    walletVolume = models.IntegerField(default=0)
    walletAddress = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f'ID: {self.user} | walletAddress: {self.walletAddress}'


class Chat(models.Model):
    firstUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="firstUser")
    secondUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="secondUser")
    visibility = models.IntegerField(default=0)
    notReadFirst = models.IntegerField(default=0)
    notReadSecond = models.IntegerField(default=0)

    def __str__(self):
        return f'ID: {self.id} | {self.firstUser} <=> {self.secondUser}'


class Message(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner")
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="chat")
    text = models.CharField(max_length=1024, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # chatId = models.IntegerField(default=0)
    # ownerLogin = models.CharField(max_length=40, blank=True)
    data = models.FileField(upload_to='messages/', blank=True)
    visibility = models.IntegerField(default=1)
    notRead = models.IntegerField(default=1)


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    search_fields = ("id", "user", "walletVolume", "walletAddress", )
    list_display = ("id", "user", "walletVolume", "walletAddress", )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    search_fields = ("id", "firstUser", "secondUser", "visibility", )
    list_display = ("id", "firstUser", "secondUser", "visibility", )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields = ("id", "chat", "owner", )
    list_display = ("id", "chat", "owner", "text", "date", )


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description", )
    list_display = ("id", "name", "description" )


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    search_fields = ("id", "userTgId", "firstNM", )
    list_display = ("id", "userTgId", "firstNM", "secondNM", "age", )


@admin.register(IpData)
class IpDataAdmin(admin.ModelAdmin):
    search_fields = ("id", "ip4", "userName", "country", "city", "language", )
    list_display = ("id", "ip4", "userName", "country", "city", "language")
