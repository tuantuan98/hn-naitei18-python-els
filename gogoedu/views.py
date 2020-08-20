from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from gogoedu.models import myUser
from django.views import generic
from django.conf import settings
from django.contrib.auth import login, authenticate


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
