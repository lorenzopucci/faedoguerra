import asyncio

from telegram.ext import Application

from faedoguerra import settings
from faedoguerra_app.telegram.commands import setup as setup_commands


class TelegramBot:
    _instance = None

    def __init__(self):
        self.application = Application\
            .builder()\
            .token(settings.TELEGRAM_BOT_TOKEN)\
            .build()

        setup_commands(self.application)


    def run_bot(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            self.application.run_polling()
        except Exception as e:
            return


    async def send_message_async(self, chat_id, text, **kwargs):
        try:
            await self.application.bot.send_message(chat_id = chat_id, text=text, **kwargs)
            return True
        except Exception as e:
            return False


    def send_message(self, chat_id, text, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(self.send_message_async(chat_id, text, **kwargs))
            return result
        except Exception as e:
            return False
        finally:
            loop.close()


    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
