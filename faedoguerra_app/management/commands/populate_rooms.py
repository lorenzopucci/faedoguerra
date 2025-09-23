from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faedoguerra import settings
from faedoguerra_app.models import Player, Room


class Command(BaseCommand):
    help = 'Populate the database with rooms and users from a csv file.'


    def add_arguments(self, parser):
        parser.add_argument('filename', nargs = '?', default = 'rooms.csv')
        parser.add_argument('--fake', action = 'store_true', help = 'Create fake users')


    def handle(self, *args, **options):
        with open(options['filename'], 'r') as rooms_file:
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

                room_obj = Room.objects.filter(label = str(number))[0]

                # create fake user
                if options['fake'] and len(data) >= 3 and len(data) < 5 and room_obj.owner is None:
                    data += [''] * 2
                    data[3] = 'Anonimo'
                    data[4] = number

                if len(data) < 5:
                    continue

                if not User.objects.filter(first_name = data[3], last_name = data[4]):
                    self.stdout.write(f'Creating user {data[3]} {data[4]}')

                    username = f'{data[3]} {data[4]}'.replace(' ', '_')
                    user = User.objects.create_user(username, '', settings.FAKE_USER_PASSWORD)

                    user.first_name = data[3]
                    user.last_name = data[4]
                    user.save()

                    player = Player(user = user, university = data[2])
                    player.save()

                    room_obj.owner = player
                    room_obj.current_owner = player
                    room_obj.save()


        self.stdout.write(self.style.SUCCESS('Successfully added new rooms and users'))
