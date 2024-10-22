from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from messenger.models import MessageModel
from messenger.schema.message import Message
from messenger.data_mappers import message_model_to_schema, message_schema_to_model
from typing import List


class SqlAlchemyMessageRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def add(self, message: Message) -> Message:
        message_model = message_schema_to_model(message)
        self._db.add(message_model)
        await self._db.commit()
        await self._db.refresh(message_model)
        return message_model_to_schema(message_model)

    async def get_by_id(self, id: int) -> Message:
        message_model = (
            await self._db.scalars(select(MessageModel).where(MessageModel.id == id))
        ).one_or_none()

        if not message_model:
            return None

        return message_model_to_schema(message_model)

    async def get_all(self, from_id: int, to_id: int) -> List[Message]:
        message_models = await self._db.scalars(
            select(MessageModel).where(
                (MessageModel.from_id == from_id) & (MessageModel.to_id == to_id)
            )
        )

        return [
            message_model_to_schema(message_model) for message_model in message_models
        ]

    async def modify(self, id: int, **kwargs) -> Message:
        message_model = (
            await self._db.scalars(select(MessageModel).where(MessageModel.id == id))
        ).one_or_none()

        if message_model is None:
            return None

        for key, value in kwargs.items():
            setattr(message_model, key, value)

        await self._db.commit()
        return message_model_to_schema(message_model)

    async def delete(self, id: int):
        message_model = (
            await self._db.scalars(select(MessageModel).where(MessageModel.id == id))
        ).one_or_none()

        if message_model is None:
            return None

        await self._db.delete(message_model)
        await self._db.commit()
