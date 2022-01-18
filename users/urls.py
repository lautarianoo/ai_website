from django.urls import path
from .views import *

urlpatterns = [
    path('login', userloginview, name='login'),
    path('register', userregisterview, name='register'),
    path('logout', logoutview, name='logout'),
    path('settings', userupdateview, name='settings')
]