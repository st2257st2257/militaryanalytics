from django.urls import path

from users.views import \
    login, \
    registration, \
    profile, \
    logout, \
    chat, \
    addMessage

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('chat/', chat, name='chat'),
    path('addMessage/<str:chatAddress>/<str:value>/', addMessage, name='addMessage'),
]
