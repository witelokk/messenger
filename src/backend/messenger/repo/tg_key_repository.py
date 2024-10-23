from typing import Protocol

from messenger.schema.tg_key import TgKey


class TgKeyRepository(Protocol):
    async def add(self, tg_key: TgKey):
        pass
