# @Aleksandr Kristal v0.0.1 || get user
from django.urls import path

from sitedata.views import \
    index_add_version, \
    index_get

app_name = 'sitedata'

urlpatterns = [
    path('versions/', index_add_version),
    path('get/', index_get),
]
