from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('catagory/', views.CatagoryListView.as_view(), name='catagory'),
	path('catagory/<int:pk>', views.CatagoryDetailView.as_view(), name='lesson'),
]
