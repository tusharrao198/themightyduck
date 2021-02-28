from django.shortcuts import render
from eduapp.models import *


def home(request):
    query = Quiz.objects.all()
    print("QUERY",query)
    query=query[0]
    context = {
        "name" : query.name,
        "desc": query.description,
        "time": query.time_created,
        "title": "Home",
    }
    return render(request, 'eduapp/home.html', context)
def signup(request):
    query = Quiz.objects.all()
    print("QUERY",query)
    query=query[0]
    context = {
        "name" : query.name,
        "desc": query.description,
        "time": query.time_created,
        "title": "Sign Up",
    }
    return render(request, 'eduapp/signup.html', context)
def login(request):
    query = Quiz.objects.all()
    print("QUERY",query)
    query=query[0]
    context = {
        "name" : query.name,
        "desc": query.description,
        "time": query.time_created,
        "title": "Login",
    }
    return render(request, 'eduapp/login.html', context)
def welcome(request):
    query = Quiz.objects.all()
    print("QUERY",query)
    query=query[0]
    context = {
        "name" : query.name,
        "desc": query.description,
        "time": query.time_created,
        "title": "Welcome",
    }
    return render(request, 'eduapp/welcome.html', context)