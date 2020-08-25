from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import myUser
from .models import Catagory,Lesson,Word,Test,Question,Choice,UserTest
# Register your models here.
admin.site.register(myUser)

admin.site.register(Catagory)
admin.site.register(Lesson)
admin.site.register(Word)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserTest)
