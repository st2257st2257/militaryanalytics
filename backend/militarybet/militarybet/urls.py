"""
URL configuration for militarybet project.

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

from mainapp.views import index_page, index_test, index_tgbot
from users.views import index_wallet
from orders.views import index_order


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='indexPage'),
    path('test/', index_test, name='testPage'),
    path('tgbot/', index_tgbot, name='tgbot'),
    path('order/', include('orders.urls', namespace='orders')),
    path('wallet/', index_wallet, name='indexWallet'),
    path('user/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
