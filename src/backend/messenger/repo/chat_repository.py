from typing import Protocol

from messenger.schema.chat import Chat


class ChatRepository(Protocol):
    async def get_by_user(self, user_id: int) -> list[Chat]:
        pass
