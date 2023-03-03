from dataclasses import dataclass


@dataclass
class UpdateObject:
    user_id: int
    chat_id: int
    body: str
    object_id: int


@dataclass
class Update:
    type: str
    object: UpdateObject


@dataclass
class Message:
    user_id: int
    text: str
    chat_id: int
