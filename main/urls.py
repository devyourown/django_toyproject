from django.urls import path
from . import views

urlpatterns= [
    path('', views.login, name='main_login'),
    path('login', views.login, name='main_login'),
    path('error', views.error, name='main_error'),
    path('index', views.index, name="main_index"),
    path('index/download', views.download, name='main_download'),
    path('logout/', views.logout, name="main_logout"),
]