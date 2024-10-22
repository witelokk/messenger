from fastapi import APIRouter, status, HTTPException

from messenger.dependencies import chat_service_dependency, session_dependency
from messenger.schema.chat import ChatsResponse


router = APIRouter()


@router.get("/")
async def get_chats(
    chat_service: chat_service_dependency, session: session_dependency
) -> ChatsResponse:
    return await chat_service.get_chats(session.user_id)
