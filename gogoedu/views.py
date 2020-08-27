from django.contrib.auth.decorators import login_required
from django.core.mail.backends import console
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm
from gogoedu.models import myUser, Lesson, Word,Catagory,Test,UserTest,Question,Choice,UserAnswer
from django.views import generic
from django.conf import settings
from django.template import loader
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.forms.models import model_to_dict

from .forms import RegisterForm, UserUpdateForm
from gogoedu.models import myUser, Lesson, Word, Catagory, UserWord

from PIL import Image


from django.shortcuts import get_object_or_404
from django.db import transaction

from django.core.exceptions import PermissionDenied
def index(request):
    return render(request, 'index.html')


def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response

class Profile(LoginRequiredMixin,generic.DetailView):
    model = myUser  
    def get_context_data(self, **kwargs):
        object_list = myUser.objects.filter()
        context = super(Profile, self).get_context_data(object_list=object_list, **kwargs)
        user = self.request.user
        if not user.avatar:
            avatar = '/media/images/profile_pics/default.jpg'
        else:
            avatar = user.avatar.url
        context['avatar'] = avatar
        return context


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


class Lesson_detail(generic.DetailView, MultipleObjectMixin):
    model = Lesson
    paginate_by = 20

    def get_success_url(self):
        return reverse('lesson-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        object_list = Word.objects.filter(lesson=self.get_object())
        context = super(Lesson_detail, self).get_context_data(object_list=object_list, **kwargs)
        return context

class CatagoryListView(generic.ListView):
    model = Catagory
    paginate_by = 6
    def get_queryset(self, **kwargs):
        try:
            name = self.request.GET.get('name',)
        except:
            name = ''
        if name:
            object_list = self.model.objects.filter(name__icontains = name)
        else:
            object_list = self.model.objects.filter()
        return object_list


class CatagoryDetailView(generic.DetailView, MultipleObjectMixin):
    model = Catagory
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = self.object.lesson_set.all()
        context = super(CatagoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


@login_required
def profile_update(request, pk):
    user = get_object_or_404(myUser, pk=pk)
    if not user.avatar:
        avatar = '/media/images/profile_pics/default.jpg'
    else:
        avatar = user.avatar.url
    if request.user == user:
        if request.method == "POST":
            form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account was updated!')
                return redirect('profile-update', pk)
        else:
            form = UserUpdateForm(instance=user)

        return render(request, 'gogoedu/myuser_update.html', {'form': form, 'avatar': avatar})
    else:
        return redirect('index')

def is_authenticated(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
def test_detail_view(request, pk):
    is_authenticated(request)
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue
            question_id = key.split('-')[1]
            choice_id = request.POST.get(key)
            data[question_id] = choice_id
        perform_test(request.user, data, test)
        return redirect(reverse('show_results', args=(test.id,)))
    return render(request, 'gogoedu/test_detail.html', context={'test': test})


class SuspiciousOperation(Exception):
    def __init__(self,value):
        print(value)


def perform_test(user, data, test):
    with transaction.atomic():
        UserAnswer.objects.filter(user=user,
                                  question__test=test).delete()
        for question_id, choice_id in data.items():
            question = Question.objects.get(id=question_id)
            choice_id = int(choice_id)
            if choice_id not in question.choice_set.values_list('id', flat=True):
                raise SuspiciousOperation('Choice is not valid for this question')
            UserAnswer.objects.create(user=user,
                                      question=question,
                                      choice_id=choice_id,
            )


def calculate_score(user, test):
    questions = Question.objects.filter(test=test)
    correct_choices = UserAnswer.objects.filter(
        user=user,
        question__test=test,
        choice__correct=True
    )
    score=UserTest(user=user,test=test,correct_answer_num=correct_choices.count())
    score.save()
    return correct_choices.count()


def show_results(request, pk):
    is_authenticated(request)
    test = Test.objects.get(id=pk)
    choices = UserAnswer.objects.filter(
        user=request.user,
        question__test=test,
    )
    listchoices=[]
    for choices1 in choices:
        listchoices.append(choices1.choice) 
    return render(request, 'gogoedu/show_results.html', {
        'test': test,
        'score': calculate_score(request.user, test),
        'choices':listchoices,
    })

class MarkLearned(generic.View):
    def post(self, request, pk, wordid):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        user_word = UserWord()
        user_word.user = myUser.objects.get(id=request.user.id)
        user_word.word = Word.objects.get(id=wordid)
        if not UserWord.objects.filter(user=request.user.id, word=wordid).first():
            user_word.save()
            learned = True
        else:
            UserWord.objects.filter(user=request.user.id, word=wordid).delete()
            learned = False
        return JsonResponse({'word': model_to_dict(user_word), 'learned': learned}, status=200)
