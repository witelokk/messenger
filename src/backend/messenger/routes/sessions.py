from fastapi import APIRouter, HTTPException, status

from messenger.schema.session import SessionResponse, CreateSessionRequest
from messenger.service.auth_service import InvalidCredentialsError
from messenger.dependencies import auth_service_dependency


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(
    create_session_request: CreateSessionRequest, auth_service: auth_service_dependency
) -> SessionResponse:
    try:
        return await auth_service.create_session(create_session_request)
    except InvalidCredentialsError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid username or password")
