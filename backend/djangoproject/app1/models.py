# @Aleksandr Kristal v0.0.1 || add email form
import datetime

from django.db import models
from django.contrib import admin

def getToken(login):
    return login + str(datetime.datetime.now())[:19]


class UserFile(models.Model):
    class_name = models.CharField(max_length=255, blank=False) #  User, Product
    user_owner = models.CharField(max_length=255, blank=False) # user1, user2, user3
    object_type = models.CharField(max_length=255, blank=True) # img, excel, pdf,
    file_name = models.CharField(max_length=255, blank=True)   # name of the file in database
    file_static_url = models.CharField(max_length=255, blank=True)
    file_image = models.ImageField(upload_to='fileImages/')
    file_data = models.FileField(upload_to='fileData/')
    visibility = models.IntegerField(default=1)


class News(models.Model):
    name = models.CharField(max_length=255, blank=False)
    photoLink = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    date = models.CharField(max_length=1024, blank=True)
    type = models.IntegerField(default=0)
    userId = models.IntegerField(default=0)


class Worker(models.Model):
    firstNM = models.CharField(max_length=20, blank=False)
    secondNM = models.CharField(max_length=20, blank=False)
    salary = models.IntegerField(default=0)
    salary_old = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.secondNM} {self.firstNM}'


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    fileData = models.FileField(upload_to='fileData/')

    def __str__(self):
        return self.title


class CustomForm(models.Model):
    title = models.CharField(max_length=1024, blank=True)
    data = models.CharField(max_length=1024, blank=True)


class EmailForm(models.Model):
    title = models.CharField(max_length=1024, blank=True)
    name = models.CharField(max_length=1024, blank=True)
    email = models.CharField(max_length=1024, blank=True)
    phone = models.CharField(max_length=1024, blank=True)
    company = models.CharField(max_length=1024, blank=True)
    message = models.CharField(max_length=1024, blank=True)


@admin.register(UserFile)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "file_name", "class_name", "user_owner", "object_type", "file_static_url",)
    list_display = ("id", "user_owner", "file_name", "object_type", "class_name")
