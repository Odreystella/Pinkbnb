import datetime
from django import template
from reservations.models import BookedDay

register = template.Library()

@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)  # BookedDay의 day는 datefield이고, 파라미터인 day는 Day class임
        BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except BookedDay.DoesNotExist:
        return False
