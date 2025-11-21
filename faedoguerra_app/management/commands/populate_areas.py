from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faedoguerra_app.models import Room


class Command(BaseCommand):
    help = 'Populate the database with common spaces from a csv file.'


    def add_arguments(self, parser):
        parser.add_argument('filename', nargs = '?', default = 'data/areas.txt')


    def handle(self, *args, **options):
        with open(options['filename'], 'r') as areas_file:
            for line in areas_file.read().splitlines():
                data = line.split(',')

                if len(data) < 5:
                    continue

                if not Room.objects.filter(floor = data[0], svg_id = data[1]):
                    self.stdout.write(f'Creating area "{data[4]}" at floor {data[0]} with svg_id {data[1]}')

                    room = Room(
                        type = data[4],
                        label = data[5],
                        tooltip = data[6],
                        floor = data[0],
                        svg_id = data[1],
                    )
                    room.save()

        self.stdout.write(self.style.SUCCESS('Successfully added new areas'))
