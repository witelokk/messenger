import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from messenger.service.auth_service import AuthService
from messenger.models import BaseModel

from .mock.mock_session_repository import MockSessionRepository
from .mock.mock_user_repository import MockUserRepository


@pytest_asyncio.fixture()
async def async_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def mock_user_repo():
    return MockUserRepository()


@pytest.fixture
def mock_session_repo():
    return MockSessionRepository()


@pytest.fixture
def auth_service(mock_user_repo, mock_session_repo):
    return AuthService(
        user_repository=mock_user_repo, session_repository=mock_session_repo
    )
