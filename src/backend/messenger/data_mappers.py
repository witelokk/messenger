from messenger.models import UserModel, MessageModel
from messenger.schema.user import User
from messenger.schema.message import Message


def user_model_to_schema(user_model: UserModel) -> User:
    return User.model_validate(user_model, from_attributes=True)


def user_schema_to_model(user: User) -> UserModel:
    return UserModel(**user.model_dump())


def message_model_to_schema(message_model: MessageModel) -> Message:
    return Message.model_validate(message_model, from_attributes=True)


def message_schema_to_model(message: Message) -> MessageModel:
    return MessageModel(**message.model_dump())
