from django.contrib import admin

# Register your models here.
from mainapp.models import IpData, TgUser

admin.site.register(IpData)
admin.site.register(TgUser)
