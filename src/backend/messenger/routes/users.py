from fastapi import APIRouter, HTTPException, status

from messenger.service.message_service import UserDoesNotExistError
from messenger.service.user_service import (
    UserAlreadyExistsError,
    AnotherUserModificationError,
)
from messenger.schema.user import CreateUserRequest, UserResponse
from messenger.schema.error import Error
from messenger.dependencies import user_service_dependency, session_dependency


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest, user_service: user_service_dependency
) -> None:
    try:
        await user_service.create_user(create_user_request)
    except UserAlreadyExistsError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "User with such username already exists"
        )


@router.get(
    "/username/{username}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
async def get_user_by_username(
    username: str, user_service: user_service_dependency, session: session_dependency
) -> UserResponse:
    try:
        return await user_service.get_user_by_username(session.user_id, username)
    except UserDoesNotExistError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"User with username {username} does not exist"
        )


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
async def get_user(
    user_id: int, user_service: user_service_dependency, session: session_dependency
) -> UserResponse:
    try:
        return await user_service.get_user(session.user_id, user_id)
    except UserDoesNotExistError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"User with id {user_id} does not exist"
        )


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Error},
    },
)
async def delete_user(
    user_id: int, user_service: user_service_dependency, session: session_dependency
) -> None:
    try:
        await user_service.delete_user(session.user_id, user_id)
    except AnotherUserModificationError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot delete another user")
