from dataclasses import dataclass
from app.store.database.database import db
from sqlalchemy import Column, TEXT, INTEGER, BOOLEAN


class Game(db):
    __tablename__ = "Games"
    id = Column(INTEGER, primary_key=True)
    chat_id = Column(INTEGER, nullable=False)
    players = Column(INTEGER, nullable=False)
    word = Column(TEXT, nullable=False)


class Players(db):
    __tablename__ = "Players"
    id = Column(INTEGER, primary_key=True)
    first_name = Column(TEXT, nullable=False)
    last_name = Column(TEXT)


class Statistics(db):
    __tablename__ = "Statistics"
    player_id = Column(INTEGER, primary_key=True)
    losses = Column(INTEGER, default=0)
    winner = Column(INTEGER, default=0)


class CurrentStatus(db):
    __tablename__ = "CurrentStatus"
    player_id = Column(INTEGER, primary_key=True)
    in_game = Column(BOOLEAN, nullable=False)


class Words(db):
    __tablename__ = "Words"
    id = Column(INTEGER, primary_key=True)
    word = Column(TEXT, nullable=False)


@dataclass
class UpdateObject:
    id: int
    user_id: int
    body: str


@dataclass
class Update:
    type: str
    object: UpdateObject


@dataclass
class Message:
    user_id: int
    text: str
