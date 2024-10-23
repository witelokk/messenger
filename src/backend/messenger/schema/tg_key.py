from datetime import datetime
from pydantic import BaseModel


class TgKey(BaseModel):
    key: str
    user_id: int
    expires: datetime
