from django.urls import path
from rooms.views import enter_home

app_name = "core"

urlpatterns = [
    path("", enter_home, name="home"),
]
