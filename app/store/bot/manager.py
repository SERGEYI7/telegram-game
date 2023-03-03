import typing
from logging import getLogger

from app.store.vk_api.dataclasses import Message, Update, UpdateObject

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")
        self.machine = 0

    async def handle_updates(self, updates: list[UpdateObject]):
        for update in updates:
            await self.app.store.vk_api.send_message(
                Message(
                    chat_id=update.chat_id,
                    user_id=update.user_id,
                    text=update.body,
                )
            )
