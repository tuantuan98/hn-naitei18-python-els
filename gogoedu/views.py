from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from gogoedu.models import Catagory, Lesson, Word
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
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
class CatagoryListView(generic.ListView):
    model = Catagory
    paginate_by = 2
class CatagoryDetailView(generic.DetailView):
    model = Catagory
    paginate_by = 2
