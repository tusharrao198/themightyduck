from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome/", views.welcome, name="welcome"),
]
