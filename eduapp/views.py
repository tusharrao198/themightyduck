from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User


def home(request):

    context = {
        "title": "Home",
    }
    return render(request, "eduapp/home.html", context)


def welcome(request):
    context = {
        "title": "Welcome",
    }
    return render(request, "eduapp/welcome.html", context)