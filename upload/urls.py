from django.urls import path
from . import views

urlpatterns = [
    path('fileView', views.fileView, name='upload_fileView'),
    path('file', views.file, name='upload_file')
]