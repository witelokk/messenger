from datetime import datetime

from aiogram import Bot

from messenger.websocket_manager import WebSocketManager
from messenger.repo.user_repository import UserRepository
from messenger.repo.message_repository import MessageRepository
from messenger.schema.message import (
    Message,
    CreateMessageRequest,
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
        tg_bot: Bot,
    ):
        self._user_repository = user_repository
        self._message_repository = message_repository
        self._websocket_manager = websocket_manager
        self._tg_bot = tg_bot

    async def create_message(
        self, user_id: int, create_message_request: CreateMessageRequest
    ):
        to_user = await self._user_repository.get_by_id(create_message_request.to_id)

        if to_user is None or not to_user.active:
            raise UserDoesNotExistError(user_id)

        message = Message(
            from_id=user_id,
            to_id=create_message_request.to_id,
            text=create_message_request.text,
            created_at=datetime.now(),
        )
        await self._message_repository.add(message)

        await self._websocket_manager.send_message(message)

        if not self._websocket_manager.is_connected(to_user.id) and to_user.telegram_id:
            user = await self._user_repository.get_by_id(user_id)
            await self._tg_bot.send_message(
                chat_id=to_user.telegram_id,
                text=f"New message from {user.username}",
            )

    async def get_messages(
        self,
        user_id: int,
        to_id: int,
    ) -> MessagesResponse:
        messages = await self._message_repository.get_all(user_id, to_id)
        return MessagesResponse(count=len(messages), messages=messages)
