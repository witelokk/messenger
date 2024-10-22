from fastapi import FastAPI
from messenger.routes import users, sessions, messages, chats, websocket


app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["auth"])
app.include_router(sessions.router, prefix="/sessions", tags=["auth"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(websocket.router, prefix="/websocket", tags=["websocket"])
