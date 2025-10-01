from django.core.management.base import BaseCommand

from faedoguerra_app.models import Room, RoomConnection


class Command(BaseCommand):
    help = 'Populate the database with room connections from a csv file.'


    def add_arguments(self, parser):
        parser.add_argument('filename', nargs = '?', default = 'connections.csv')


    def add_connection(self, from_floor, from_svg_id, to_floor, to_svg_id):
        from_room = Room.objects.get(floor = from_floor, svg_id = from_svg_id)
        to_room = Room.objects.get(floor = to_floor, svg_id = to_svg_id)

        if not RoomConnection.objects.filter(room1 = from_room, room2 = to_room):
            self.stdout.write(f"Creating connection {from_room.tooltip} -> {to_room.tooltip}")

            connection = RoomConnection(room1 = from_room, room2 = to_room)
            connection.save()


    def handle(self, *args, **options):
        with open(options['filename'], 'r') as areas_file:
            for line in areas_file.read().splitlines():
                data = line.split(',')

                if len(data) < 4:
                    continue

                self.add_connection(data[0], data[1], data[2], data[3])
                self.add_connection(data[2], data[3], data[0], data[1])

        self.stdout.write(self.style.SUCCESS('Successfully added new connections'))
