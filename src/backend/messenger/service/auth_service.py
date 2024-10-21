from datetime import datetime, timedelta
from hashlib import sha256
from uuid import uuid4

from messenger.repo import SessionRepository, UserRepository
from messenger.schema.user import CreateUserRequest, User
from messenger.schema.session import CreateSessionRequest, Session, SessionResponse


def _hash_password(password: str):
    return sha256(password.encode()).hexdigest()


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(
        self, user_repository: UserRepository, session_repository: SessionRepository
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository

    async def create_user(self, create_user_request: CreateUserRequest):
        if (
            await self._user_repository.get_by_username(create_user_request.username)
            is not None
        ):
            raise UserAlreadyExistsError()

        user = User(
            active=True,
            username=create_user_request.username,
            password_hash=_hash_password(create_user_request.password),
        )
        await self._user_repository.add(user)

    async def delete_user(self, user_id: int):
        await self._user_repository.modify(user_id, active=False)
        await self._session_repository.delete_all(user_id)

    async def create_session(
        self, create_session_request: CreateSessionRequest
    ) -> Session:
        user = await self._user_repository.get_by_username(
            create_session_request.username
        )

        if (
            user == None
            or user.password_hash != _hash_password(create_session_request.password)
            or not user.active
        ):
            raise InvalidCredentialsError()

        token = uuid4().hex

        session = Session(
            token=token,
            user_id=user.id,
            expires=datetime.now() + timedelta(seconds=1200),
        )
        await self._session_repository.add(session)

        return SessionResponse(
            token=token,
            user_id=user.id,
            username=user.username,
            expires_at=session.expires,
        )
