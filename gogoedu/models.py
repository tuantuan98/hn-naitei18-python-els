from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image


class Catagory(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/lesson_pics', blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('lesson', args=[str(self.id)])


class Lesson(models.Model):
    catagory = models.ForeignKey('Catagory',on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null= True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('lesson-detail', args=[str(self.id)])


class Word(models.Model):
    catagory = models.ForeignKey('Catagory',on_delete=models.SET_NULL, null=True)
    word = models.CharField(max_length=255)
    mean = models.CharField(max_length=255,null=True, blank=True)

    CHOICES = (
        ('V', 'Verb'),
        ('N', 'Noun'),
        ('Adj','Adjective'),
    )
    type = models.CharField(max_length=10,choices=CHOICES)
    lesson = models.ManyToManyField(Lesson)

    def __str__(self):
        """String for representing the Model object."""
        return self.word


class Test(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True)
    question_num = models.IntegerField()
    name = models.CharField(max_length=50)
    time = models.IntegerField(default=600)
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('test-detail', args=[str(self.id)])
    def get_test_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('test-detail', args=[str(self.id)])

class Question(models.Model):
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True)
    question_text = models.CharField(max_length=255)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.choice_text


class myUser(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile_pics', blank=True)
    email = models.EmailField(_('email address'))

    # Resize the image
    # def save(self):
    #     super().save()
    #
    #     image = Image.open(self.avatar.path)
    #     # To resize the profile image
    #     if image.height > 400 or image.width > 400:
    #         output_size = (400, 400)
    #         image.thumbnail(output_size)
    #         image.save(self.avatar.path)


class UserTest(models.Model):
    user = models.ForeignKey('myUser', on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    correct_answer_num = models.IntegerField(default=0)
    def __str__(self):
        """String for representing the Model object."""
        return self.test.name

class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey('myUser', on_delete=models.CASCADE)



class UserWord(models.Model):
    user = models.ForeignKey('myUser', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    memoried = models.BooleanField(null=False,default=False)
