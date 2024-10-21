from messenger.schema.user import User


class MockUserRepository:
    def __init__(self):
        self.users = {}
        self.current_id = 1

    async def get_by_id(self, id: int) -> User | None:
        return self.users.get(id)

    async def get_by_username(self, username: str) -> User | None:
        return next(
            (user for user in self.users.values() if user.username == username), None
        )

    async def add(self, user: User) -> User:
        user.id = self.current_id
        self.users[self.current_id] = user
        self.current_id += 1
        return user

    async def modify(self, id: int, **kwargs) -> User | None:
        user = self.users.get(id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.users[id] = user
        return user

    async def delete(self, id: int) -> User | None:
        return self.users.pop(id, None)
