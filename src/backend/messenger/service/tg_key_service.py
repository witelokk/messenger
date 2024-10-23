from datetime import datetime, timedelta
from uuid import uuid4
from messenger.repo.tg_key_repository import TgKeyRepository
from messenger.schema.tg_key import TgKey


KEY_TTL = timedelta(seconds=60)


class TgKeyService:
    def __init__(self, tg_key_repository: TgKeyRepository):
        self._tg_key_repository = tg_key_repository

    async def create_key(self, user_id: int) -> TgKey:
        tg_key = TgKey(
            key=uuid4().hex,
            user_id=user_id,
            expires=datetime.now() + KEY_TTL,
        )

        await self._tg_key_repository.add(tg_key)

        return tg_key
