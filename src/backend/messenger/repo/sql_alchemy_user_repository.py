from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from messenger.models import UserModel
from messenger.schema.user import User
from messenger.data_mappers import user_model_to_schema, user_schema_to_model


class SqlAlchemyUserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_id(self, id: int) -> User:
        user_model = (
            await self._db.scalars(select(UserModel).where(UserModel.id == id))
        ).one_or_none()
        return user_model_to_schema(user_model)

    async def get_by_username(self, username: str) -> User:
        user_model = (
            await self._db.scalars(
                select(UserModel).where(UserModel.username == username)
            )
        ).one_or_none()
        return user_model_to_schema(user_model)

    async def add(self, user: User) -> User:
        user_model = user_schema_to_model(user)
        self._db.add(user_model)
        await self._db.commit()
        return user_model

    async def modify(self, id: int, **kwargs) -> User:
        user_model = (
            await self._db.scalars(select(UserModel).where(UserModel.id == id))
        ).one_or_none()

        if user_model is None:
            return None

        for key, value in kwargs.items():
            setattr(user_model, key, value)

        await self._db.commit()
        return user_model_to_schema(user_model)

    async def delete(self, id: int) -> User:
        user_model = (
            await self._db.scalars(select(UserModel).where(UserModel.id == id))
        ).one_or_none()

        if user_model is None:
            return None

        await self._db.delete(user_model)
        await self._db.commit()
        return user_model_to_schema(user_model)
