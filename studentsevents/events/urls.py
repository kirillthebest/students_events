from django.urls import path
from .views import *

urlpatterns = [
    path('', auth, name='auth'),
    path('events', show_events_page, name='events_page'),
    path('student', show_student_page, name='student_page'),
    path('teacher', show_teacher_page, name='teacher_page'),
    path('logout', logout, name='logout'),
    path('participate/<int:event_id>', participate, name='participate'),
    path('event/upload', upload_event_document, name='upload_event_document')
]