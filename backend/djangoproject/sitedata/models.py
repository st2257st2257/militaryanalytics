# @Aleksandr Kristal v0.0.2 || add
from datetime import datetime
from django.contrib import admin

from django.db import models


class SiteBlock(models.Model):
    name = models.CharField(max_length=50, blank=False)
    value = models.TextField(blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=False)
    versionSmall = models.IntegerField(default=0)
    versionMiddle = models.IntegerField(default=0)
    versionBig = models.IntegerField(default=0)

    def getVersion(self):
        return str(self.versionBig) + "." + \
               str(self.versionMiddle) + "." + \
               str(self.versionSmall)


    def updateVersion(self):
        self.version = self.getVersion()


    def addSmall(self, value, description):
        self.versionSmall += 1
        self.value = value
        self.description = description
        self.updateVersion()


    def addMiddle(self, value, description):
        self.versionSmall = 0
        self.versionMiddle += 1
        self.value = value
        self.description = description
        self.updateVersion()


    def addBig(self, value, description):
        self.versionSmall = 0
        self.versionMiddle = 0
        self.versionBig += 1
        self.value = value
        self.description = description
        self.updateVersion()

    def __str__(self):
        return f'ID: {self.id} | Name: {self.name}'


@admin.register(SiteBlock)
class SiteBlockAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "value", "description", )
    list_display = ("id", "name", "value", )


class SiteBlockVersionList(models.Model):
    name = models.CharField(max_length=50, blank=False)
    value = models.TextField(blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=False)


@admin.register(SiteBlockVersionList)
class SiteBlockVersionListAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "value", "description", )
    list_display = ("id", "name", "version", )
