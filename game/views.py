from django.shortcuts import render


def index(request):
    return render(request, 'game/index.html')


def room(request, pk):
    return render(request, "game/room.html", {"room_name": pk})
