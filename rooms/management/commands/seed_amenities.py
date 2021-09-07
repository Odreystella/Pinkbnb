from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command creates amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="How many times do you want me to tell you that I love you?",
    #     )

    def handle(self, *args, **options):
        amenities = [
            "Hair dryer",
            "Shampoo",
            "Conditioner",
            "Body soap",
            "Hot water",
            "Free washer – In unit",
            "Essentials",
            "Hangers",
            "Bed linens",
            "Iron",
            "Air conditioning",
            "Heating",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Fire extinguisher",
            "Wifi – 500 Mbps",
            "Available throughout the listing",
            "Dedicated workspace",
            "Kitchen",
            "Refrigerator",
            "Microwave",
            "Cooking basics",
            "Dishes and silverware",
            "Freezer",
            "Induction stove",
            "Coffee maker: Nespresso",
            "Private entrance",
            "Luggage dropoff allowed",
            "Long term stays allowed",
            "Self check-in",
            "Smart lock",
        ]
        for name in amenities:
            Amenity.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS("Amenities created!"))
