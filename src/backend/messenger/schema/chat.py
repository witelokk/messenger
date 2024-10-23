from pydantic import BaseModel

from .user import User, UserResponse
from .message import Message


class Chat(BaseModel):
    to_user: User
    last_message: Message


class ChatResponse(BaseModel):
    to_user: UserResponse
    last_message: Message


class ChatsResponse(BaseModel):
    count: int
    chats: list[ChatResponse]
