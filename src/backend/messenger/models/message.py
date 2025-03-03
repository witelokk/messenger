from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class MessageModel(BaseModel):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(String())
    created_at: Mapped[int] = mapped_column(DateTime(), server_default=func.now())
