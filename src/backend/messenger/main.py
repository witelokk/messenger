from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from messenger.routes import users, sessions, messages, chats, websocket, tg_key


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router, prefix="/sessions", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(tg_key.router, prefix="/tg_key", tags=["Telegram integration"])
app.include_router(websocket.router, prefix="/websocket", tags=["Websockets"])