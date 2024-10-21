from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from messenger.schema.session import Session
from messenger.settings import settings
from messenger.repo.redis_session_repository import RedisSessionRepository
from messenger.repo.user_repository import UserRepository
from messenger.repo.session_repository import SessionRepository
from messenger.service.auth_service import AuthService
from messenger.repo.sql_alchemy_user_repository import SqlAlchemyUserRepository
from messenger.db import SessionLocal


async def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def get_user_repository(db: db_dependency):
    return SqlAlchemyUserRepository(db)


user_repository_dependency = Annotated[UserRepository, Depends(get_user_repository)]


async def get_redis():
    return Redis(
        host=settings.redis_host, port=settings.redis_port, decode_responses=True
    )


redis_dependency = Annotated[Redis, Depends(get_redis)]


async def get_session_repository(redis: redis_dependency):
    return RedisSessionRepository(redis)


session_repository_dependency = Annotated[
    SessionRepository, Depends(get_session_repository)
]


async def get_auth_service(
    user_repository: user_repository_dependency,
    session_repository: session_repository_dependency,
):
    return AuthService(user_repository, session_repository)


auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_session(
    token: Annotated[
        str,
        Depends(
            oauth2_bearer,
        ),
    ],
    session_repository: session_repository_dependency,
):
    session = await session_repository.get(token)

    if not session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return session


session_dependency = Annotated[Session, Depends(get_session)]
