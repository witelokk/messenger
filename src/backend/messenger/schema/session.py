from typing import Annotated
from pydantic import BaseModel, Field

from datetime import datetime


class Session(BaseModel):
    token: str
    expires: datetime
    user_id: int


class CreateSessionRequest(BaseModel):
    username: str
    password: str


class SessionResponse(BaseModel):
    token: Annotated[str, Field()]
    user_id: int
    username: str
    expires_at: datetime
