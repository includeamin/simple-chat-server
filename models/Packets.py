from pydantic import BaseModel
from typing import Any
from datetime import datetime


class Packet(BaseModel):
    state: str
    data: dict


class LoginDataModel(BaseModel):
    username: str
    sid: str


class ErrorDataModel(BaseModel):
    description: str


class DirectMessageDataModel(BaseModel):
    token: str
    receiver: str
    content_type: str
    content: Any
    create_at: datetime = datetime.now().timestamp()


class MessagePacket(BaseModel):
    id: int = None
    sender_username: str
    receiver_username: str
    content_type: str
    content: Any
    create_at: datetime = datetime.now()


class SeenModel(BaseModel):
    id: int
