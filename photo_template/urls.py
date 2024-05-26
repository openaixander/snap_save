from django.urls import path

from . import views

app_name  = 'photo_template'


urlpatterns = [
    path('', views.index, name='index'),
    path('selection/', views.selection, name='selection'),
    path('photographer_dashboard/', views.p_dashboard, name='p_dashboard'),
    path('client_dashboard/', views.c_dashboard, name='c_dashboard'),
    path('search_token/', views.search_token, name='search_token'),
    path('search/', views.searched_folder, name='searched_folder')
]