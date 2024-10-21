from datetime import datetime

from pydantic import BaseModel

from .user import UserResponse


class Message(BaseModel):
    from_id: int
    to_id: int
    text: str
    created_at: datetime
    id: int = None


class CreateMessageRequest(BaseModel):
    to_id: int
    text: str


class MessageResponse(BaseModel):
    id: int
    from_user: UserResponse
    to_user: UserResponse
    text: str
    created_at: datetime


class MessagesResponse(BaseModel):
    count: int
    messages: list[MessageResponse]
