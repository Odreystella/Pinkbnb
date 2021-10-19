from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from .models import List


@login_required
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = List.objects.get_or_create(user=request.user, name="My Favourites Houses")
        if action == 'add':
            the_list.rooms.add(room)
        elif action == 'remove':
            the_list.rooms.remove(room) 
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))