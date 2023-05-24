from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class StudentGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'


class EventType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    event_type = models.ForeignKey(EventType, null=True, default=None, on_delete=models.CASCADE,
                                   verbose_name='тип мероприятия')
    event_date = models.DateField(null=True, verbose_name='Дата мероприятия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='пользователь')
    group = models.ForeignKey(StudentGroup, null=True, blank=True, on_delete=models.CASCADE, verbose_name='учебная группа')
    events = models.ManyToManyField(Event, verbose_name='Мероприятия')

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + " " + self.user.last_name
        return self.user.username

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class ProfileEvent(models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, verbose_name='Студент')
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name='Мероприятие')
    score = models.IntegerField(verbose_name='Баллы')

    def __str__(self):
        if self.profile.user.first_name or self.profile.user.last_name:
            username = self.profile.user.first_name + " " + self.profile.user.last_name
        username = self.profile.user.username
        return 'Мероприятие ' + self.event.name + " (" + username + ")"

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
