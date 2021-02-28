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
        "title": "Home",
    }
    return render(request, 'eduapp/signup.html', context)