from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faedoguerra import settings
from faedoguerra_app.models import Player, Room


class Command(BaseCommand):
    help = 'Populate the database from a rooms.csv file.'

    def handle(self, *args, **options):

        with open('rooms.csv', 'r') as rooms_file:
            for number, line in enumerate(rooms_file.read().splitlines()):
                number += 1
                data = line.split(',')

                if len(data) < 2:
                    continue

                if not Room.objects.filter(label = str(number)):
                    self.stdout.write(f'Creating room {number} at floor {data[0]} with svg_id {data[1]}')

                    room = Room(
                        type = 'c',
                        label = str(number),
                        tooltip = f'Camera {number}',
                        floor = data[0],
                        svg_id = data[1],
                    )
                    room.save()

                if len(data) < 5:
                    continue

                if not User.objects.filter(first_name = data[2], last_name = data[3]):
                    self.stdout.write(f'Creating user {data[2]} {data[3]}')

                    username = f'{data[2]} {data[3]}'.replace(' ', '_')
                    user = User.objects.create_user(username, '', settings.FAKE_USER_PASSWORD)

                    user.first_name = data[2]
                    user.last_name = data[3]
                    user.save()

                    player = Player(
                        user = user,
                        university = data[4],
                    )
                    player.save()

                    room = Room.objects.filter(label = str(number))[0]
                    room.owner = player
                    room.current_owner = player
                    room.save()


        self.stdout.write(self.style.SUCCESS('Successfully populated room database'))
