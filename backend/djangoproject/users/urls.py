# @Aleksandr Kristal v0.0.1 || get user
from django.urls import path

from users.views import \
    index_form, \
    index_chat, \
    index_register, \
    index_recovery, \
    index_send_email, \
    index_get, \
    index_get_completeness, \
    index_get_partners

app_name = 'users'

urlpatterns = [
    path('form/', index_form),
    path('chat/', index_chat),
    path('register/', index_register),
    path('recovery/', index_recovery),
    path('sendemail/', index_send_email),
    path('get_partners/', index_get_partners),
    path('get/', index_get),
    path('completeness', index_get_completeness)
]