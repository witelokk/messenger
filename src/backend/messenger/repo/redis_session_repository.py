from datetime import datetime

from redis.asyncio import Redis

from messenger.schema.session import Session


SESSION_PREFIX = "session"
SESSION_USER_ID_KEY = b"user_id"
SESSION_EXPIRES_KEY = b"expires"


class RedisSessionRepository:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def add(self, session: Session):
        name = f"{SESSION_PREFIX}:{session.user_id}:{session.token}"
        await self._redis.hset(name, SESSION_USER_ID_KEY, session.user_id)
        await self._redis.hset(name, SESSION_EXPIRES_KEY, session.expires.timestamp())
        await self._redis.expireat(name, session.expires)

    async def get(self, token: str):
        pattern = f"{SESSION_PREFIX}:*:{token}"

        try:
            name = (await self._redis.keys(pattern))[0]
        except IndexError:
            return None

        if not await self._redis.exists(name):
            return None

        user_id, expires_timestamp = await self._redis.hmget(
            name, [SESSION_USER_ID_KEY, SESSION_EXPIRES_KEY]
        )
        return Session(
            token=token,
            user_id=int(user_id),
            expires=datetime.fromtimestamp(float(expires_timestamp)),
        )

    async def delete_all(self, user_id: int) -> None:
        pattern = f"{SESSION_PREFIX}:{user_id}:*"
        keys = await self._redis.keys(pattern)
        await self._redis.delete(*keys)
