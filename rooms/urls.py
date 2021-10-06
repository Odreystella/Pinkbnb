from django.urls import path
from .views import RoomDetailView, SearchView, EditRoomView, CreateRoomView


app_name = "rooms"

urlpatterns = [
    path("create/", CreateRoomView.as_view(), name="create"),
    path("<int:pk>/", RoomDetailView.as_view(), name="detail"),
    path("search/", SearchView.as_view(), name="search"),
    path("<int:pk>/edit/", EditRoomView.as_view(), name="edit"),
]