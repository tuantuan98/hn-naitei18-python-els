from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('profile/<int:pk>', views.Profile.as_view(), name='profile-detail'),
]
