"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import index_wallet


from app1.views import index_page, \
    index_news, \
    index_get, \
    index_set, \
    index_checkSettings, \
    upload_photo, \
    form_add, \
    form_email, \
    upload_file, \
    get_file, \
    index_make_default, \
    index_kafka_send, \
    index_kafka_get

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='indexPage'),
    path('make_default/', index_make_default, name='indexdef'),
    path('kafka_start/', index_kafka_send),
    path('kafka_get/', index_kafka_get),
    path('wallet/', index_wallet, name='indexWallet'),
    path('order/', include('orders.urls', namespace='orders')),
    path('form/add/<str:title>/<str:data>/', form_add, name='form_add'),
    path('form/email/<str:title>/<str:name>/<str:email>/<str:phone>/<str:company>/<str:message>', form_email, name='form_add'),
    path('user/', include('users.urls', namespace='users')),
    path('sitedata/', include('sitedata.urls', namespace='sitedata')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
