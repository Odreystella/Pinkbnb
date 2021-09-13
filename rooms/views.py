from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.http import Http404
from .models import Room


class HomeView(ListView):

    """ HomeView Definition """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room":room})

    except Room.DoesNotExist:
        return redirect(reverse("core:home"))
