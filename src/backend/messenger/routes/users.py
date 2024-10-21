from fastapi import APIRouter, HTTPException, status

from messenger.service.auth_service import UserAlreadyExistsError
from messenger.schema.user import CreateUserRequest
from messenger.dependencies import auth_service_dependency, session_dependency


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest, auth_service: auth_service_dependency
) -> None:
    try:
        await auth_service.create_user(create_user_request)
    except UserAlreadyExistsError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "User with such username already exists"
        )


@router.delete("/me")
async def delete_user(
    auth_service: auth_service_dependency, session: session_dependency
) -> None:
    await auth_service.delete_user(session.user_id)
