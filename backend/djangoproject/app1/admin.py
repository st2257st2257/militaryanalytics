# @Aleksandr Kristal v0.0.1 || add email form
from django.contrib import admin
from app1.models import Worker
from app1.models import News
from app1.models import Post
from app1.models import CustomForm
from app1.models import EmailForm


# Register your models here.


admin.site.register(Worker)
admin.site.register(News)
admin.site.register(Post)
admin.site.register(CustomForm)
admin.site.register(EmailForm)
