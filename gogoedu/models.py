from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Catagory(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        """String for representing the Model object."""
        return self.name



class Lesson(models.Model):
    catagory=models.ForeignKey('Catagory',on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=255)
    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Word(models.Model):
    catagory=models.ForeignKey('Catagory',on_delete=models.SET_NULL, null=True)
    word=models.CharField(max_length=255)
    mean=models.CharField(max_length=255,null=True, blank=True)

    CHOICES = (
        ('V', 'Verb'),
        ('N', 'Noun'),
        ('Adj','Adjective'),
    )
    type=models.CharField(max_length=10,choices=CHOICES)
    lesson=models.ManyToManyField(Lesson)
    def __str__(self):
        """String for representing the Model object."""
        return self.word


class Test(models.Model):
    lesson=models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True)
    question_num=models.IntegerField()
    time=models.TimeField()

class Question(models.Model):
    test=models.ForeignKey('Test', on_delete=models.SET_NULL, null=True)
    question_text=models.CharField(max_length=255)
    def __str__(self):
        """String for representing the Model object."""
        return self.question_text


class Choice(models.Model):
    choice_text=models.CharField(max_length=255)
    question=models.ForeignKey('Question', on_delete=models.CASCADE)
    is_true=models.BooleanField(default=False)
    def __str__(self):
        """String for representing the Model object."""
        return self.choice_text

class myUser(AbstractUser):
    avatar=models.CharField(max_length=255,null=True)


class UserTest(models.Model):
    user=models.ForeignKey('myUser', on_delete=models.CASCADE)
    test=models.ForeignKey('Test', on_delete=models.CASCADE)
    correct_answer_num=models.IntegerField(default=0)

class UserWord(models.Model):
    user=models.ForeignKey('myUser', on_delete=models.CASCADE)
    word=models.ForeignKey('Word', on_delete=models.CASCADE)
    memoried=models.BooleanField(default=True)
