from django.shortcuts import render
from .models import Room


def enter_home(request):
    all_rooms = Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
