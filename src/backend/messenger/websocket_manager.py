from collections import defaultdict
from fastapi import WebSocket

from messenger.schema.message import Message


class WebSocketManager:
    def __init__(self):
        self._websockets: dict[int, list[WebSocket]] = defaultdict(lambda: [])

    def register(self, user_id: int, websocket: WebSocket):
        self._websockets[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self._websockets[user_id].remove(websocket)

    def is_connected(self, user_id: int) -> bool:
        return len(self._websockets[user_id]) > 0

    async def send_message(self, message: Message):
        for ws in self._websockets[message.to_id] + self._websockets[message.from_id]:
            await ws.send_json(
                {
                    "event": "new_message",
                    "new_message": {
                        "to_id": message.to_id,
                        "from_id": message.from_id,
                        "text": message.text,
                        "created_at": message.created_at.timestamp(),
                    },
                }
            )
