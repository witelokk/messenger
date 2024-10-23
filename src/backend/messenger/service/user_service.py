from messenger.repo import SessionRepository, UserRepository
from messenger.security import hash_password
from messenger.schema.user import CreateUserRequest, User, UserResponse


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotEsistError(Exception):
    pass


class AnotherUserModificationError(Exception):
    pass


class UserService:
    def __init__(
        self, user_repository: UserRepository, session_repository: SessionRepository
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository

    async def create_user(self, create_user_request: CreateUserRequest):
        if (
            await self._user_repository.get_by_username(create_user_request.username)
            is not None
        ):
            raise UserAlreadyExistsError()

        user = User(
            active=True,
            username=create_user_request.username,
            password_hash=hash_password(create_user_request.password),
        )
        await self._user_repository.add(user)

    async def get_user(self, user_id: int, id: int) -> UserResponse:
        user = await self._user_repository.get_by_id(id)

        if not user:
            raise UserAlreadyExistsError()

        return UserResponse(id=user.id, username=user.username, active=user.active)

    async def get_user_by_username(self, user_id: int, username: str) -> UserResponse:
        user = await self._user_repository.get_by_username(username)

        if not user:
            raise UserAlreadyExistsError()

        return UserResponse(id=user.id, username=user.username, active=user.active)

    async def delete_user(self, user_id: int, id: int):
        if user_id != id:
            raise AnotherUserModificationError()

        await self._user_repository.modify(user_id, active=False)
        await self._session_repository.delete_all(user_id)
