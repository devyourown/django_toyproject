from django.urls import path
from . import views

urlpatterns = [
    path('email', views.email, name='signup_email'),
    path('verifyView', views.verifyView, name="signup_verifyView"),
    path('verify', views.verify, name="signup_verify"),
    path('verified', views.verified, name="signup_verified"),
    path('', views.signup, name="signup"),
]