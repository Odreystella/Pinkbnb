from django.views.generic import ListView
from .models import Room


class HomeView(ListView):

    """ HomeView Definition """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    page_kwarg = "room"