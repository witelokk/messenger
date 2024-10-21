from fastapi import APIRouter, HTTPException, status


from messenger.dependencies import (
    message_service_dependency,
    session_dependency,
    # websocket_manager_dependency,
    session_repository_dependency,
)
from messenger.service.message_service import UserDoesNotExistError
from messenger.schema.message import MessagesResponse, CreateMessageRequest


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_message(
    message_service: message_service_dependency,
    create_message_request: CreateMessageRequest,
    session: session_dependency,
) -> None:
    try:
        await message_service.create_message(session.user_id, create_message_request)
    except UserDoesNotExistError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"User with id {e.user_id} does not exist")


@router.get("/to/{to_id}")
async def get_messages_to(
    message_service: message_service_dependency,
    session: session_dependency,
    to_id: int,
) -> MessagesResponse:
    return await message_service.get_messages(session.user_id, to_id)
