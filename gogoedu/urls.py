import dajax
from django.urls import path
from django.views.decorators.http import require_POST

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register, name='register'),
	path('profile/<int:pk>', views.Profile.as_view(), name='profile-detail'),
	path('lesson/<int:pk>', views.Lesson_detail.as_view(), name='lesson-detail'),
	path('lesson/<int:pk>/words/<int:wordid>/learned/', views.MarkLearned.as_view(), name='mark-learned'),
	path('catagory/', views.CatagoryListView.as_view(), name='catagory'),
	path('catagory/<int:pk>', views.CatagoryDetailView.as_view(), name='lesson'),
	path('profile/<int:pk>/edit', views.profile_update, name='profile-update'),
	path('test/<int:pk>', views.test_detail_view, name='test-detail'),
	path('results/<int:pk>', views.show_results, name='show_results'),
]
