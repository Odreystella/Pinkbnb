import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms.models import Room
from users.models import User
from lists.models import List

NAME = "lists"


class Command(BaseCommand):

    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        rooms = Room.objects.all()
        users = User.objects.all()
        seeder.add_entity(
            List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()  # 딕셔너리 형태의 생성된 list pk가 담겨 있음
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = List.objects.get(pk=pk)
            random_room = rooms[random.randint(0, 5) : random.randint(6, 20)]
            list_model.rooms.add(*random_room)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
