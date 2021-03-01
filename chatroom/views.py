from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render


def index(request):
    return render(request, "chatroom/index.html", {})


def room(request, room_name):
    return render(request, "chatroom/room.html", {"room_name": room_name})
