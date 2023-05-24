from django.urls import path
from .views import *

urlpatterns = [
    path('', show_login_page, name='login_page'),
    path('auth', auth, name='auth'),
    path('events', show_events_page, name='events_page'),
    path('student', show_student_page, name='student_page'),
    path('teacher', show_teacher_page, name='teacher_page')
]