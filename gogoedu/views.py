from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from gogoedu.models import myUser, Lesson, Word,Catagory
from django.views import generic
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.template import loader
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import MultipleObjectMixin
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

class Profile(generic.DetailView):
    model = myUser


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

class Lesson_detail(generic.DetailView,MultipleObjectMixin):
    model = Lesson
    paginate_by = 20
    def get_context_data(self, **kwargs):
        object_list = Word.objects.filter(lesson=self.get_object())
        context = super(Lesson_detail, self).get_context_data(object_list=object_list, **kwargs)
        return context
class CatagoryListView(generic.ListView):
    model = Catagory
    paginate_by = 4
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
    
class CatagoryDetailView(generic.DetailView,MultipleObjectMixin):
    model = Catagory
    paginate_by = 10
    def get_context_data(self, **kwargs):
        object_list = self.object.lesson_set.all()
        context = super(CatagoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
