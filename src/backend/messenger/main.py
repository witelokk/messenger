from fastapi import FastAPI
from messenger.routes import (users, sessions)


app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["auth"])
app.include_router(sessions.router, prefix="/sessions", tags=["auth"])