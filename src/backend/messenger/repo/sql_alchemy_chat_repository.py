from messenger.data_mappers import user_model_to_schema
from sqlalchemy import and_, case, desc, func, or_, select, text
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from messenger.models import MessageModel, UserModel

from messenger.schema.chat import Chat
from messenger.schema.message import Message
from messenger.schema.user import User


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
SELECT 
    lm.id AS last_message_id, 
    lm.from_id AS last_message_from_id, 
    lm.to_id AS last_message_to_id, 
    lm.text AS last_message_text, 
    lm.created_at AS last_message_created_at,
    u.id AS chat_partner_id, 
    u.username AS chat_partner_username, 
    u.password_hash AS chat_partner_password_hash, 
    u.telegram_id AS chat_partner_telegram_id, 
    u.active AS chat_partner_active
FROM last_messages lm
JOIN user_chats uc
  ON (lm.from_id = :user_id AND lm.to_id = uc.chat_partner)
  OR (lm.to_id = :user_id AND lm.from_id = uc.chat_partner)
JOIN users u
  ON u.id = uc.chat_partner
ORDER BY lm.created_at DESC;
"""


class SqlAlchemyChatRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_user(self, user_id: int) -> list[Chat]:
        chats = (await self._db.execute(text(CHATS_QUERY), {"user_id": user_id})).all()

        return [
            Chat(
                to_user=User(
                    id=chat_partner_id,
                    username=chat_partner_username,
                    password_hash=chat_partner_password_hash,
                    active=chat_partner_active,
                    telegram_id=chat_partner_telegram_id,
                ),
                last_message=Message(
                    id=last_message_id,
                    from_id=last_message_from_id,
                    to_id=last_message_to_id,
                    text=last_message_text,
                    created_at=last_message_created_at,
                ),
            )
            for (
                last_message_id,
                last_message_from_id,
                last_message_to_id,
                last_message_text,
                last_message_created_at,
                chat_partner_id,
                chat_partner_username,
                chat_partner_password_hash,
                chat_partner_telegram_id,
                chat_partner_active,
            ) in chats
        ]
