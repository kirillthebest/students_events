from django.db import models


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)


# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255)
