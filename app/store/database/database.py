from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import re

from app.store.database import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        # url = self.app.config.database.
        compile_re = re.compile(r"sqlalchemy\.url = (.*)")
        database_name = self.app.config.database.database
        host = self.app.config.database.host
        user = self.app.config.database.user
        port = self.app.config.database.port
        password = self.app.config.database.password
        url_db = rf"postgresql+asyncpg://{user}:{password}@{host}/{database_name}"
        print(url_db)
        self._engine = create_async_engine(url_db)
        _session = sessionmaker(
            bind=self._engine, expire_on_commit=False, class_=AsyncSession
        )
        # with _session as session:
        self.session = _session
        print("Connect finish")

    async def disconnect(self, *_: list, **__: dict) -> None:
        return
        await self.session.close()
        # raise NotImplemented
