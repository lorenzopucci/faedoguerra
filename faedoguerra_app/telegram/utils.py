from faedoguerra import settings
from faedoguerra_app.telegram.bot import TelegramBot
from faedoguerra_app.models import Player


def send_message(chat_id, text):
    bot = TelegramBot.get_instance()
    return bot.send_message(chat_id, text)


def send_message_to_channel(text):
    send_message(settings.TELEGRAM_CHANNEL_ID, text)


def broadcast_message(text):
    chat_ids = Player.objects\
        .filter(chat_id = ~0)\
        .values_list('chat_id', flat = True)

    for chat_id in chat_ids:
        send_message(chat_id, text)
