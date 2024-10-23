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


class MessagesResponse(BaseModel):
    count: int
    messages: list[Message]
