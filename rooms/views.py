from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, View
from django.http import Http404
from django_countries import countries
from .models import Room, RoomType, Amenity, Facility, HouseRule


class HomeView(ListView):

    """ HomeView Definition """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetailView(DetailView):

    """ RoomDetail Definition """

    model = Room


def search(request, **kwargs):
    city = request.GET.get("city", "Anywhere")
    city = city.title()
    s_country = request.GET.get("country", "KR")
    s_room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    s_house_rules = request.GET.getlist("house_rules")

    form = {
        "city": city,
        "s_country": s_country,
        "s_room_type": s_room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "super_host": super_host,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "s_house_rules": s_house_rules,
    }
    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()
    house_rules = HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }
    return render(request, "rooms/search.html", {**form, **choices})


class EditRoomView(UpdateView):

    """EditRoomView Definition"""

    model = Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",  
        "description",  
        "country",  
        "city", 
        "price", 
        "address", 
        "guests", 
        "beds", 
        "baths",
        "bedrooms", 
        "check_in",
        "check_out", 
        "instant_book", 
        "room_type", 
        "amenities",
        "facilities", 
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        # if room.host.pk != self.request.user.pk:
            # raise Http404() 
        return room



