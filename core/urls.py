from django.urls import path
from rooms.views import HomeView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
