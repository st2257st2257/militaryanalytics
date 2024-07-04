from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    walletVolume = models.IntegerField(default=0)
    walletAddress = models.CharField(max_length=250, blank=True)


class Chat(models.Model):
    firstUserLogin = models.CharField(max_length=40, blank=True)
    secondUserLogin = models.CharField(max_length=40, blank=True)
    firstUserName = models.CharField(max_length=40, blank=True)
    secondUserName = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=40, blank=True)
    visibility = models.IntegerField(default=0)


class Message(models.Model):
    text = models.CharField(max_length=1024, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    chatId = models.IntegerField(default=0)
    ownerLogin = models.CharField(max_length=40, blank=True)
    data = models.FileField(upload_to='messages/', blank=True)
    visibility = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.text} {self.date}'
