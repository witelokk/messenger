from messenger.models import UserModel
from messenger.schema.user import User


def user_model_to_schema(user_model: UserModel):
    return User.model_validate(user_model, from_attributes=True)


def user_schema_to_model(user: User):
    return UserModel(**user.model_dump())
