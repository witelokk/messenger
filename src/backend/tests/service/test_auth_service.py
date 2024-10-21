import pytest
from messenger.schema.user import CreateUserRequest
from messenger.schema.session import CreateSessionRequest
from messenger.service.auth_service import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    _hash_password,
)


@pytest.mark.asyncio
async def test_create_user(auth_service, mock_user_repo):
    create_user_request = CreateUserRequest(username="testuser", password="password123")

    await auth_service.create_user(create_user_request)

    user = await mock_user_repo.get_by_username("testuser")
    assert user is not None
    assert user.username == "testuser"
    assert user.password_hash == _hash_password("password123")


@pytest.mark.asyncio
async def test_create_user_already_exists(auth_service):
    create_user_request = CreateUserRequest(username="testuser", password="password123")
    await auth_service.create_user(create_user_request)

    with pytest.raises(UserAlreadyExistsError):
        await auth_service.create_user(create_user_request)


@pytest.mark.asyncio
async def test_create_session_success(auth_service, mock_session_repo):
    create_user_request = CreateUserRequest(username="testuser", password="password123")
    await auth_service.create_user(create_user_request)

    create_session_request = CreateSessionRequest(
        username="testuser", password="password123"
    )
    session = await auth_service.create_session(create_session_request)

    assert session is not None
    assert session.user_id == 1
    assert session.token is not None

    stored_session = await mock_session_repo.get(session.token)
    assert stored_session is not None
    assert stored_session.token == session.token
    assert stored_session.user_id == 1


@pytest.mark.asyncio
async def test_create_session_invalid_credentials(auth_service):
    create_user_request = CreateUserRequest(username="testuser", password="password123")
    await auth_service.create_user(create_user_request)

    create_session_request = CreateSessionRequest(
        username="testuser", password="wrongpassword"
    )

    with pytest.raises(InvalidCredentialsError):
        await auth_service.create_session(create_session_request)


@pytest.mark.asyncio
async def test_create_session_user_does_not_exist(auth_service):
    create_session_request = CreateSessionRequest(
        username="nonexistentuser", password="password"
    )

    with pytest.raises(InvalidCredentialsError):
        await auth_service.create_session(create_session_request)
