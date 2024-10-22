from pydantic import BaseModel

from .user import UserResponse
from .message import Message, MessageResponse


class Chat(BaseModel):
    to_id: int
    last_message: Message


class ChatResponse(BaseModel):
    to_user: UserResponse
    last_message: MessageResponse


class ChatsResponse(BaseModel):
    count: int
    chats: list[ChatResponse]
