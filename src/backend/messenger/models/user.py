from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(), unique=True)
    password_hash: Mapped[str] = mapped_column(String())
    telegram_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean(), server_default="1")
