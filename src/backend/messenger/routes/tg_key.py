from fastapi import APIRouter

from messenger.dependencies import tg_key_serice_dependency, session_dependency
from messenger.schema.tg_key import TgKey


router = APIRouter()


@router.post("")
async def create_key(tg_key_service: tg_key_serice_dependency, session: session_dependency) -> TgKey:
    return await tg_key_service.create_key(session.user_id)
