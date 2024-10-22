from typing import Protocol

from messenger.schema.message import Message


class MessageRepository(Protocol):
    async def add(self, message: Message) -> Message:
        pass

    async def get_by_id(self, id: int) -> Message:
        pass

    async def get_all(self, from_id: int, to_id: int) -> list[Message]:
        pass

    async def modify(self, id: int, **kwargs) -> Message:
        pass

    async def delete(self, id: int):
        pass
