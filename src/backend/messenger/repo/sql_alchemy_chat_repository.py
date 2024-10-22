from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from messenger.schema.chat import Chat
from messenger.schema.message import Message


CHATS_QUERY = """
WITH user_chats AS (
    SELECT
        CASE
            WHEN from_id = :user_id THEN to_id
            ELSE from_id
        END AS chat_partner,
        MAX(created_at) AS last_message_time
    FROM messages
    WHERE from_id = :user_id OR to_id = :user_id
    GROUP BY chat_partner
),
last_messages AS (
    SELECT m.*
    FROM messages m
    JOIN user_chats uc
      ON (m.from_id = :user_id AND m.to_id = uc.chat_partner)
      OR (m.to_id = :user_id AND m.from_id = uc.chat_partner)
    WHERE m.created_at = uc.last_message_time
)
SELECT id, from_id, to_id, text, created_at
FROM last_messages
ORDER BY created_at DESC;
"""


class SqlAlchemyChatRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_user(self, user_id: int) -> list[Chat]:
        chats = await self._db.execute(text(CHATS_QUERY), {"user_id": user_id})

        return [
            Chat(
                to_id=last_message_from_id + last_message_to_id - user_id,
                last_message=Message(
                    id=id,
                    from_id=last_message_from_id,
                    to_id=last_message_to_id,
                    text=last_message_text,
                    created_at=last_message_created_at,
                ),
            )
            for (
                id,
                last_message_from_id,
                last_message_to_id,
                last_message_text,
                last_message_created_at,
            ) in chats
        ]
