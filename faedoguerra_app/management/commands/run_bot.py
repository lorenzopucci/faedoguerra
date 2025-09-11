from datetime import datetime

from django.core.management.base import BaseCommand

from faedoguerra_app.telegram.bot import TelegramBot


class Command(BaseCommand):
    help = 'Runs the telegram bot in polling mode.'

    def handle(self, *args, **options):
        now = datetime.now()
        self.stdout.write(self.style.HTTP_INFO('Starting telegram bot at %s.' % now.strftime('%d/%m/%Y, %H:%M')))

        bot = TelegramBot.get_instance()
        bot.run_bot()

        now = datetime.now()
        self.stdout.write(self.style.HTTP_INFO('Shut down telegram bot at %s.' % now.strftime('%d/%m/%Y, %H:%M')))
