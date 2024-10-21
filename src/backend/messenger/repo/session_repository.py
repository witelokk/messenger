from typing import Protocol

from messenger.schema.session import Session


class SessionRepository(Protocol):
    async def add(self, session: Session) -> None:
        pass

    async def get(self, token: str) -> Session:
        pass
