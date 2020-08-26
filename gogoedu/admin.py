from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import myUser
from .models import Catagory,Lesson,Word,Test,Question,Choice,UserTest,UserWord
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.
admin.site.register(myUser)
admin.site.register(Catagory)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'catagory', 'description')
    list_filter = ('name', 'catagory')

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Word)

class ChoiceInline(NestedStackedInline):
    model = Choice
    extra = 1
class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    show_change_link = True
    inlines = [ChoiceInline,]
class TestAdmin(NestedModelAdmin):
    list_display = ('question_num', 'name', 'lesson', 'time')
    list_filter = ('name', 'question_num', 'lesson' )
    inlines = [QuestionInline,]

admin.site.register(Test, TestAdmin)

class QuestionAdmin(NestedModelAdmin):
    list_display = ('test', 'question_text')
    inlines = [ChoiceInline,]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(UserTest)
admin.site.register(UserWord)


