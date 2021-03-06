import datetime
from django.db import models
from django.utils import timezone
from core.models import AbstractTimeStamped


class BookedDay(models.Model):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="booked_day")

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


class Reservation(AbstractTimeStamped):
    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reservations",
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reservations",
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now < self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:           # 새로운 reservation 인스턴스 이면 BookedDay obj 만들어줌
            start = self.check_in
            end = self.check_out
            gap = end - start
            existing_booked_day = BookedDay.objects.filter(reservation__room=self.room, day=start).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)    # create reservation instance first
                for i in range(gap.days):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
