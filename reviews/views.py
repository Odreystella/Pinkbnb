from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from rooms.models import Room
from .forms import CreateReviewForm



def create_review(request, room_pk):
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        room = Room.objects.get_or_none(pk=room_pk)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Review Uploaded")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))