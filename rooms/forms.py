from django import forms
from django_countries.fields import CountryField
from .models import Amenity, Facility, RoomType, Room


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(required=False, empty_label="Any kind", queryset=RoomType.objects.all())
    price = forms.IntegerField(required=False, min_value=1, max_value=300)
    guests = forms.IntegerField(required=False, min_value=1, max_value=10)
    bedrooms = forms.IntegerField(required=False, min_value=1, max_value=5)
    beds = forms.IntegerField(required=False, min_value=1, max_value=5)
    baths = forms.IntegerField(required=False, min_value=1, max_value=5)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(required=False, queryset=Amenity.objects.all(), widget=forms.CheckboxSelectMultiple)
    facilities = forms.ModelMultipleChoiceField(required=False, queryset=Facility.objects.all(), widget=forms.CheckboxSelectMultiple)


