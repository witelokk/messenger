from typing import Protocol

from messenger.schema.user import User


class UserRepository(Protocol):
    async def get_by_id(self, id: int) -> User:
        pass

    async def get_by_username(self, username: str) -> User:
        pass

    async def add(self, user: User) -> User:
        pass

    async def modify(self, id, **kwargs) -> User:
        pass

    async def delete(self, id: int):
        pass
