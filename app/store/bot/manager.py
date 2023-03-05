import typing
from logging import getLogger
from enum import Enum

from app.store.vk_api.dataclasses import Message, Update, UpdateObject

if typing.TYPE_CHECKING:
    from app.web.app import Application


class State(str, Enum):
    player_recruitment = "start"
    end_player_recruitment = "end"



class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")
        self.machine = 0
        self.update = UpdateObject
        self.state = None

    async def handle_updates(self, updates: list[UpdateObject]):
        for update in updates:
            text = update.body
            # state = State().player_recruitment
            print(text)
            self.update = update
            if text == State.player_recruitment.value:
                await self.player_recruitment()
                await self.app.store.vk_api.send_message(
                    Message(
                        chat_id=self.update.chat_id,
                        user_id=self.update.user_id,
                        text="Начался набор игроков",
                    )
                )
                # TODO state +1
            elif State.end_player_recruitment.value:
                # TODO Заканчивать набор игроков.
                # TODO state +1
                pass


    async def player_recruitment(self):
        # TODO Создание игровой сессии в таблице GameSession
        # TODO добавление пользователя отправившего start добавить в поле host таблицы GameSession
        # TODO набор игроков может закрыть только host либо по достижению максимума игроков
        pass



