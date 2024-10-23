from messenger.schema.user import UserResponse
from messenger.repo.user_repository import UserRepository
from messenger.schema.chat import ChatResponse, ChatsResponse
from messenger.repo.chat_repository import ChatRepository


class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self._chat_repository = chat_repository

    async def get_chats(self, user_id: int) -> ChatsResponse:
        chats = await self._chat_repository.get_by_user(user_id)
        return ChatsResponse(
            count=len(chats),
            chats=[
                ChatResponse(
                    to_user=UserResponse(
                        id=chat.to_user.id,
                        username=chat.to_user.username,
                        active=chat.to_user.active,
                    ),
                    last_message=chat.last_message,
                )
                for chat in chats
            ],
        )
