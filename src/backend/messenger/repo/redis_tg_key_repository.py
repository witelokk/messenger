from redis.asyncio import Redis

from messenger.schema.tg_key import TgKey


TG_KEY_PREFIX = "tg_key"


class RedisTgKeyRepository:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def add(self, tg_key: TgKey):
        name = f"{TG_KEY_PREFIX}:{tg_key.key}"
        await self._redis.set(name, tg_key.user_id)
        await self._redis.expireat(name, tg_key.expires)
