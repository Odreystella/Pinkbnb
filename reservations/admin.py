from django.contrib import admin
from .models import Reservation, BookedDay


@admin.register(BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    """ BookedDay Admin Definition """
    
    list_display = (
        "day", "reservation"
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)
