from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    path("search/", views.SearchView.as_view(), name="search"),
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("<int:pk>/", views.DetailRoomView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
]