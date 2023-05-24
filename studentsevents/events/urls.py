from django.urls import path
from .views import *

urlpatterns = [
    path('', show_login_page, name='login_page'),
    path('auth', auth, name='auth')
]