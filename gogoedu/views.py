from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.conf import settings
from django.template import loader
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, UserUpdateForm
from gogoedu.models import myUser, Lesson, Word, Catagory

from PIL import Image


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
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


class Lesson_detail(generic.DetailView, MultipleObjectMixin):
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


@login_required
def profile_update(request, pk):
    user = get_object_or_404(myUser, pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account was updated!')
                return redirect('profile-update', pk)
        else:
            form = UserUpdateForm(instance=user)

        return render(request, 'gogoedu/myuser_update.html', {'form': form})
    else:
        return redirect('index')


