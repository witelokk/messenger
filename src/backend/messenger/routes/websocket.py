from fastapi import Query, WebSocket, APIRouter, WebSocketDisconnect, WebSocketException

from messenger.dependencies import (
    session_repository_dependency,
    websocket_manager_dependency,
)


router = APIRouter()


@router.websocket("")
async def websocket_endpoint(
    websocket_manager: websocket_manager_dependency,
    websocket: WebSocket,
    session_repository: session_repository_dependency,
    token: str = Query(...),
):
    session = await session_repository.get(token)

    if session is None:
        raise WebSocketException(3000, "Invalid token")

    websocket_manager.register(session.user_id, websocket)
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(session.user_id, websocket)
