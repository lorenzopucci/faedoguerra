from django.core.management.base import BaseCommand

from faedoguerra_app.models import Announcement


class Command(BaseCommand):
    help = 'Populate the database with announcements from a csv file.'


    def add_arguments(self, parser):
        parser.add_argument('filename', nargs = '?', default = 'data/announcements.txt')


    def add_announcement(self, type, text):
        if not Announcement.objects.filter(string = text):
            self.stdout.write(f'Creating announcement "{text}"')

            announcement = Announcement(type = type, string = text)
            announcement.save()


    def handle(self, *args, **options):
        with open(options['filename'], 'r') as announcements_file:
            for line in announcements_file.read().splitlines():
                data = line.split('|')

                if len(data) < 2:
                    continue

                if data[0] == 'e':
                    for before in Announcement.objects.filter(type = 'a'):
                        self.add_announcement('e', f'{before.string} {data[1]}')
                else:
                    self.add_announcement(data[0], data[1])

        self.stdout.write(self.style.SUCCESS('Successfully added new announcements'))
