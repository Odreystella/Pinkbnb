from django import template
from lists.models import List

register = template.Library()

@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    if user.is_authenticated:
        the_list = List.objects.get_or_none(user=user, name="My Favourites Houses")
        if the_list is not None:
            return room in the_list.rooms.all()
        else:
            return False
    else:
        return False
