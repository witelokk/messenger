import pytest
import pytest_asyncio
from fakeredis import FakeAsyncRedis
from datetime import datetime, timedelta
from messenger.schema.session import Session
from messenger.repo.redis_session_repository import (
    RedisSessionRepository,
    SESSION_PREFIX,
    SESSION_USER_ID_KEY,
    SESSION_EXPIRES_KEY,
)


@pytest.fixture
def test_session():
    return Session(
        token="test_token", user_id=123, expires=datetime.now() + timedelta(hours=1)
    )


@pytest_asyncio.fixture
async def fake_redis():
    redis = await FakeAsyncRedis()
    yield redis
    await redis.flushall()
    await redis.aclose()


@pytest.mark.asyncio
async def test_add_session(fake_redis, test_session):
    repository = RedisSessionRepository(fake_redis)

    await repository.add(test_session)

    session_name = f"{SESSION_PREFIX}:{test_session.user_id}:{test_session.token}"
    session_data = await fake_redis.hgetall(session_name)
    assert session_data[SESSION_USER_ID_KEY].decode() == str(test_session.user_id)
    assert float(session_data[SESSION_EXPIRES_KEY]) == test_session.expires.timestamp()

    ttl = await fake_redis.ttl(session_name)
    assert ttl > 0


@pytest.mark.asyncio
async def test_get_session_exists(fake_redis, test_session):
    repository = RedisSessionRepository(fake_redis)

    session_name = f"{SESSION_PREFIX}:{test_session.user_id}:{test_session.token}"
    await fake_redis.hset(session_name, SESSION_USER_ID_KEY, test_session.user_id)
    await fake_redis.hset(
        session_name, SESSION_EXPIRES_KEY, test_session.expires.timestamp()
    )
    await fake_redis.expireat(session_name, test_session.expires)

    session = await repository.get(test_session.token)

    assert session is not None
    assert session.token == test_session.token
    assert session.user_id == test_session.user_id
    assert session.expires == test_session.expires


@pytest.mark.asyncio
async def test_get_session_not_exists(fake_redis):
    repository = RedisSessionRepository(fake_redis)

    session = await repository.get("abc")

    assert session is None
