from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/",views.signup, name="signup"),
    path("login/",views.login, name="login"),
    path("welcome/",views.welcome, name="welcome"),
    path("register/",views.register, name="register"),
    path("validation/",views.validation, name="validation"),


]
