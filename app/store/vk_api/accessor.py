import random
import typing
from pprint import pprint
from typing import Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateObject
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_PATH = "https://api.vk.com/method/"
TELEGRAM_API_PATH = "https://api.telegram.org/bot{token}/"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None
        self.head_url = f"https://api.telegram.org/bot{self.app.config.bot.telegram_token}/"
        self.offset = None

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.poller = Poller(app.store)
        self.logger.info("start polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    def _build_query_telegram(self, method: str, params: dict):
        ready_url = (
            self.head_url
            + method
            + "?"
            + "&".join([f"{k}={v}" for k, v in params.items()])
        )
        return ready_url

    async def _get_long_poll_service(self):
        url = self._build_query(
            host=API_PATH,
            method="groups.getLongPollServer",
            params={
                "group_id": self.app.config.bot.group_id,
                "access_token": self.app.config.bot.token,
            },
        )
        async with self.session.get(url) as resp:
            data = (await resp.json()).get("response")
            self.logger.info(data)
            self.key = data["key"]
            self.server = data["server"]
            self.ts = data["ts"]
            self.logger.info(self.server)

    async def poll(self):
        build_url = self._build_query(
            TELEGRAM_API_PATH.format(token=self.app.config.bot.telegram_token),
            "getUpdates",
            {"offset": self.offset},
        )
        async with self.session.get(build_url) as resp:
            data = await resp.json()
            updates = []
            if data["ok"]:
                result = data["result"]
                if result:
                    for event in result:
                        event_id = event["update_id"]
                        self.offset = int(event_id) + 1
                        chat_id = event["message"]["chat"]["id"]
                        text = event["message"]["text"]
                        user_id = event["message"]["from"]["id"]
                        updates.append(
                            UpdateObject(
                                object_id=int(event_id),
                                user_id=user_id,
                                chat_id=chat_id,
                                body=text,
                            )
                        )
        return updates

    async def send_message(self, message: Message) -> None:
        async with self.session.get(
            self._build_query(
                TELEGRAM_API_PATH.format(token=self.app.config.bot.telegram_token),
                "sendMessage",
                params={
                    "chat_id": message.chat_id,
                    "text": message.text,
                    "user_id": message.user_id,
                },
            )
        ) as resp:
            data = await resp.json()
            self.logger.info(data)
