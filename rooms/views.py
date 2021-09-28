from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, View, FormView
from django.http import Http404
from django_countries import countries
from .models import Room, RoomType, Amenity, Facility, HouseRule
from .forms import SearchForm, CreateRoomForm

class HomeView(ListView):

    """ HomeView Definition """

    model = Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetailView(DetailView):

    """ RoomDetail Definition """

    model = Room


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):
        country = request.GET.get("country")
        city = request.GET.get("city")

        if city:

            form = SearchForm(request.GET)
            
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                
                filter_args = {}
                if city != "Anywhere":
                    filter_args["city__startswith"] = city
                
                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["guests__gte"] = bedrooms

                if beds is not None:
                    filter_args["guests__gte"] = beds

                if baths is not None:
                    filter_args["guests__gte"] = baths
                
                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["superhost"] = True

                rooms = Room.objects.filter(**filter_args)

                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)

                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)

                qs = rooms.order_by("created")

                paginator = Paginator(qs, 2)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                current_url = "".join(request.get_full_path().split("page")[0]) 
                if current_url[-1] != "&":
                    current_url = "".join(request.get_full_path().split("page")[0]) + "&"

                print("current_url: ", current_url)
                
                return render(request, "rooms/search.html", {"form": form, "page_obj": rooms, "current_url": current_url})

        else: 

            form = SearchForm()
        
        return render(request, "rooms/search.html", {"form": form})
   

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


class CreateRoomView(FormView):

    form_class = CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        # messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))