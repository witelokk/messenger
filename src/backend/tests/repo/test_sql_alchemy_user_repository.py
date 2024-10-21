import pytest
from sqlalchemy.future import select

from messenger.models import BaseModel, UserModel
from messenger.schema.user import User
from messenger.repo import SqlAlchemyUserRepository


@pytest.fixture
def test_user():
    return User(
        username="testuser",
        password_hash="testhash",
        telegram_id=12345,
    )


@pytest.fixture
def test_user_model():
    return UserModel(
        id=1,
        username="testuser",
        password_hash="testhash",
        telegram_id=12345,
    )


@pytest.mark.asyncio
async def test_get_by_id(async_session, test_user_model):
    repo = SqlAlchemyUserRepository(async_session)

    async_session.add(test_user_model)
    await async_session.commit()

    user = await repo.get_by_id(test_user_model.id)

    assert user.id == test_user_model.id
    assert user.username == test_user_model.username


@pytest.mark.asyncio
async def test_get_by_username(async_session, test_user_model):
    repo = SqlAlchemyUserRepository(async_session)

    async_session.add(test_user_model)
    await async_session.commit()

    user = await repo.get_by_username(test_user_model.username)

    assert user.username == test_user_model.username
    assert user.telegram_id == test_user_model.telegram_id


@pytest.mark.asyncio
async def test_add(async_session, test_user):
    repo = SqlAlchemyUserRepository(async_session)

    added_user = await repo.add(test_user)

    result = await async_session.scalars(
        select(UserModel).where(UserModel.username == test_user.username)
    )
    user_from_db = result.one_or_none()

    assert user_from_db is not None
    assert user_from_db.username == test_user.username
    assert user_from_db.password_hash == test_user.password_hash
    assert user_from_db.telegram_id == test_user.telegram_id


@pytest.mark.asyncio
async def test_modify(async_session, test_user_model):
    repo = SqlAlchemyUserRepository(async_session)

    async_session.add(test_user_model)
    await async_session.commit()

    updated_user = await repo.modify(test_user_model.id, username="updateduser")

    assert updated_user.username == "updateduser"

    result = await async_session.scalars(
        select(UserModel).where(UserModel.id == test_user_model.id)
    )
    user_from_db = result.one_or_none()

    assert user_from_db.username == "updateduser"


@pytest.mark.asyncio
async def test_delete(async_session, test_user_model):
    repo = SqlAlchemyUserRepository(async_session)

    async_session.add(test_user_model)
    await async_session.commit()

    deleted_user = await repo.delete(test_user_model.id)

    assert deleted_user.id == test_user_model.id

    result = await async_session.scalars(
        select(UserModel).where(UserModel.id == test_user_model.id)
    )
    user_from_db = result.one_or_none()

    assert user_from_db is None
