from typing import Annotated
from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    password_hash: str
    telegram_id: int = None
    id: int = None


class CreateUserRequest(BaseModel):
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=32,
            pattern=r"^[a-zA-Z0-9_\.]+$",
            strip_whitespace=True,
        ),
    ]
    password: Annotated[str, Field(min_length=8, max_length=64)]

    class Config:
        str_strip_whitespace = True
