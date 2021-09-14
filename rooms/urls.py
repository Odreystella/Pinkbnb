from django.urls import path
from .views import RoomDetailView, search, EditRoomView


app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", RoomDetailView.as_view(), name="detail"),
    path("search/", search, name="search"),
    path("<int:pk>/edit/", EditRoomView.as_view(), name="edit"),
]