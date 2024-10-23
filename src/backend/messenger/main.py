from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from messenger.routes import users, sessions, messages, chats, websocket


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router, prefix="/sessions", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(websocket.router, prefix="/websocket", tags=["websocket"])
