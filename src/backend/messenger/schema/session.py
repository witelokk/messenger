from pydantic import BaseModel

from datetime import datetime


class Session(BaseModel):
    token: str
    expires: datetime
    user_id: int