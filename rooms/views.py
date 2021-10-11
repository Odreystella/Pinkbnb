from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, View, FormView, CreateView
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django_countries import countries
from users.mixins import LoggedInOnlyView
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo
from .forms import SearchForm, CreatePhotoForm, CreateRoomForm

class HomeView(ListView):

    """ HomeView Definition """

    model = Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")
        city = request.GET.get("city")

        if city:

            form = SearchForm(request.GET)
            
            if form.is_valid():  # 유효성 검증을 통과한 폼 데이터는 cleaned_data에 담겨있음
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
   

class DetailRoomView(DetailView):

    """ RoomDetail Definition """

    model = Room


# Create form, Clean form, Validate form, 템플릿 렌더링, 리다이렉트(get_absolute_url) 다 해줌
class EditRoomView(LoggedInOnlyView, UpdateView):

    """ EditRoomView Definition """

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

    def get_object(self, queryset=None):   # return the object the view is displaying
        room = super().get_object(queryset=queryset)   
        if room.host.pk != self.request.user.pk:   # room의 host가 아닌 다른 유저가 수정하지 못하게끔 함
            raise Http404() 
        return room


class RoomPhotosView(LoggedInOnlyView, DetailView):

    model = Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):   # return the object the view is displaying
        room = super().get_object(queryset=queryset)   
        if room.host.pk != self.request.user.pk:   # room의 host가 아닌 다른 유저가 수정하지 못하게끔 함
            raise Http404()                        # DEBUG=False여야 내가 만든 404.html이 렌더링됨
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    print(f"Should delete {photo_pk} from {room_pk}")
    user = request.user
    try:
        # room 찾기
        room = Room.objects.get(pk=room_pk)
        # 1. user == room.host, delete photo
        if user == room.host:
            Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        # 2. user != room.host, error messages
        else:
            messages.error(request, "Photo can be deleted by host of this room.")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except Room.DoesNotExist:
        # room 없으면
        return redirect(reverse("core:home"))


class EditPhotoView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    """ EditPhotoView Definition """

    model = Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Caption of photo is updated"
    fields = ("caption",)

    def get_success_url(self):   
        """ if form_valid, save the form and return HttpResponseRedirect(self.get_success_url())"""
        room_pk = self.kwargs.get("room_pk")   # room_pk가 필요함
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class UploadPhotoView(LoggedInOnlyView, FormView):

    """ UploadPhotoView Definition """
    
    form_class = CreatePhotoForm
    template_name = "rooms/photo_create.html"

    def form_valid(self, form):
        room_pk = self.kwargs.get("pk")
        form.save(room_pk)
        messages.success(self.request, "Photo uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))


class CreateRoomView(LoggedInOnlyView, FormView):

    """ CreateRoomView Definition """

    form_class = CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()              # CreateRoomForm에서 만들어진 room을 리턴함
        room.host = self.request.user   # form 저장하기 전에 host에 인스턴스 넣어줌
        room.save()                     # 이제야 데이터베이스에 저장됨
        form.save_m2m()                 # save_m2m()은 데이터베이스에 인스턴스가 만들어져야 호출할 수 있음
        messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))