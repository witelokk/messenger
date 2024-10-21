from datetime import datetime
from messenger.schema.session import Session


class MockSessionRepository:
    def __init__(self):
        self.sessions = {}

    async def add(self, session: Session) -> None:
        self.sessions[session.token] = session

    async def get(self, token: str) -> Session | None:
        session = self.sessions.get(token)
        if session and session.expires > datetime.utcnow():
            return session
        return None
