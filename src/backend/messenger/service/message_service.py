from datetime import datetime

from messenger.websocket_manager import WebSocketManager
from messenger.repo.user_repository import UserRepository
from messenger.repo.message_repository import MessageRepository
from messenger.schema.message import (
    Message,
    CreateMessageRequest,
    MessageResponse,
    MessagesResponse,
    UserResponse,
)


class UserDoesNotExistError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id


class MessageService:
    def __init__(
        self,
        user_repository: UserRepository,
        message_repository: MessageRepository,
        websocket_manager: WebSocketManager,
    ):
        self._user_repository = user_repository
        self._message_repository = message_repository
        self._websocket_manager = websocket_manager

    async def create_message(
        self, user_id: int, create_message_request: CreateMessageRequest
    ):
        to_user = await self._user_repository.get_by_id(create_message_request.to_id)

        if to_user is None:
            raise UserDoesNotExistError(user_id)

        message = Message(
            from_id=user_id,
            to_id=create_message_request.to_id,
            text=create_message_request.text,
            created_at=datetime.now(),
        )
        await self._message_repository.add(message)
        await self._websocket_manager.send_message(message)

    async def get_messages(
        self,
        user_id: int,
        to_id: int,
    ) -> MessagesResponse:
        messages = await self._message_repository.get_all(user_id, to_id)
        message_schemas = [
            MessageResponse(
                id=message.id,
                from_user=UserResponse(
                    id=message.from_id,
                    username=(
                        await self._user_repository.get_by_id(message.from_id)
                    ).username,
                    active=(
                        await self._user_repository.get_by_id(message.from_id)
                    ).active,
                ),
                to_user=UserResponse(
                    id=message.to_id,
                    username=(
                        await self._user_repository.get_by_id(message.from_id)
                    ).username,
                    active=(
                        await self._user_repository.get_by_id(message.from_id)
                    ).active,
                ),
                text=message.text,
                created_at=message.created_at,
            )
            for message in messages
        ]
        return MessagesResponse(count=len(message_schemas), messages=message_schemas)
