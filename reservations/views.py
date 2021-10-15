import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from rooms.models import Room
from reviews.forms import CreateReviewForm
from .models import BookedDay, Reservation


class CreateError(Exception):
    pass


@login_required
def create_reservation(request, room_pk, year, month, day):
    try:
        day = datetime.datetime(year, month, day)
        room = Room.objects.get(pk=room_pk)
        BookedDay.objects.get(day=day, reservation__room=room)
        raise CreateError()    # BookedDay가 있다면 예약할 수 없으니까 error
    except (Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve this room") 
        return redirect(reverse("core:home"))
    except BookedDay.DoesNotExist:
        reservation = Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=day,
            check_out=day + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

    
class DetailReservationView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = Reservation.objects.get_or_none(pk=pk)  # create get_or_none model manager
        if not reservation or (
            reservation.guest != self.request.user 
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = CreateReviewForm()
        return render(self.request, "reservations/detail.html", {"reservation": reservation, "form": form})


def edit_reservation(request, pk, status):
    reservation = Reservation.objects.get_or_none(pk=pk)
    print(reservation) 
    if not reservation or (
        reservation.guest != request.user 
        and reservation.room.host != request.user
    ):
        raise Http404()
    if status == "confirm":
        reservation.status = Reservation.STATUS_CONFIRMED
    elif status == "cancel":
        reservation.status = Reservation.STATUS_CANCELED
        BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))