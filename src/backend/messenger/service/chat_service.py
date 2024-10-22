from messenger.schema.user import UserResponse
from messenger.repo.user_repository import UserRepository
from messenger.schema.chat import ChatResponse, ChatsResponse
from messenger.schema.message import MessageResponse
from messenger.repo.chat_repository import ChatRepository


class ChatService:
    def __init__(
        self, chat_repository: ChatRepository, user_repository: UserRepository
    ):
        self._chat_repository = chat_repository
        self._user_repository = user_repository

    async def _get_user_response(self, id: int) -> UserResponse:
        user = await self._user_repository.get_by_id(id)
        return UserResponse(id=user.id, username=user.username, active=user.active)

    async def get_chats(self, user_id: int) -> ChatsResponse:
        chats = await self._chat_repository.get_by_user(user_id)
        return ChatsResponse(
            count=len(chats),
            chats=[
                ChatResponse(
                    to_user=await self._get_user_response(chat.to_id),
                    last_message=MessageResponse(
                        id=chat.last_message.id,
                        from_user=await self._get_user_response(
                            chat.last_message.from_id
                        ),
                        to_user=await self._get_user_response(chat.last_message.to_id),
                        text=chat.last_message.text,
                        created_at=chat.last_message.created_at,
                    ),
                )
                for chat in chats
            ],
        )
