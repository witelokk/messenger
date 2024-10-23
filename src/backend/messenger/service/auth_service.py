from datetime import datetime, timedelta
from uuid import uuid4

from messenger.security import hash_password
from messenger.repo import SessionRepository, UserRepository
from messenger.schema.session import CreateSessionRequest, Session, SessionResponse


SESSION_TTL = timedelta(hours=1)


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(
        self, user_repository: UserRepository, session_repository: SessionRepository
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository

    async def create_session(
        self, create_session_request: CreateSessionRequest
    ) -> Session:
        user = await self._user_repository.get_by_username(
            create_session_request.username
        )

        if (
            user == None
            or user.password_hash != hash_password(create_session_request.password)
            or not user.active
        ):
            raise InvalidCredentialsError()

        token = uuid4().hex

        session = Session(
            token=token,
            user_id=user.id,
            expires=datetime.now() + SESSION_TTL,
        )
        await self._session_repository.add(session)

        return SessionResponse(
            token=token,
            user_id=user.id,
            username=user.username,
            expires_at=session.expires,
        )
