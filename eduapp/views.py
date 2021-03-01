from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from eduapp.models import *

def home(request):
    # query = Quiz.objects.all()
    # print("QUERY",query)
    # query=query[0]
    context = {
        # "name" : query.name,
        # "desc": query.description,
        # "time": query.time_created,
        "title": "Home",
    }
    return render(request, 'eduapp/home.html', context)
def signup(request):
    context = {
        "title": "Sign Up",
    }
    return render(request, 'eduapp/signup.html', context)

def login(request):
    context = {
        "title": "Login",
    }
    return render(request, 'eduapp/login.html', context)


def register(request):
    if request.method =="POST":
        user = request.POST.get("Username")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        query = User(
            name= user,
            email= email,
            password = password
        )
        # print("USER", query)
        query.save()
    return render(request, 'eduapp/welcome.html')

def validation(request):
    if request.method =="POST":
        user = request.POST.get("Username")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        query = User.objects.filter(name=user)
        # print("query", query[0])
        if not query.exists():
            redirect('login')
        context = {
        "user": user,
        }
    # return render(request, 'eduapp/welcome.html', context)
    return welcome(request, query)

def welcome(request, query):
    # query = User.objects.filter(name=user)
    # print("QUERY",query)
    # query=query[0]
    # print("QUERY",query[0].id)
    r=[]
    s=[]
    q = Quiz.objects.all().filter(user=query[0].id)
    for i in q:        # if q.id == r.id:
        r.append(Questions.objects.filter(quiz=i.id).count())
    print("LEN",len(r))
    context = {
        "quiz": q,
        "questions":r,
        "len": int(len(r)),
        "title": "Welcome",
    }
    return render(request, 'eduapp/welcome.html', context)
