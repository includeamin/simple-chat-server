from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
from models.Packets import MessagePacket


class SignUpUserBodyModel(BaseModel):
    username: str
    password: str

    # @validator("password")
    # def password_validator(cls, v):
    #     return str(v)


class LoginUserBodyModel(BaseModel):
    username: str
    password: str


class JwtPayloadModel(BaseModel):
    username: str
    ca: datetime = datetime.now().timestamp()
    ex: datetime = (datetime.now() + timedelta(days=7)).timestamp()


class SignUpResponseModel(BaseModel):
    Authorization: str


class LoginResponseModel(BaseModel):
    Authorization: str


class UserUnreadMessage(BaseModel):
    id: int
    sender_username: str
    content: str
    content_type: str
    create_at: datetime


class UserMessagesResponse(BaseModel):
    messages: List[UserUnreadMessage]


class UserChatHistoryModel(BaseModel):
    messages: List[MessagePacket] = []
