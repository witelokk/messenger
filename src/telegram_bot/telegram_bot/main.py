import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from redis import Redis
import asyncpg


from settings import settings


dp = Dispatcher()
form_router = Router()


async def handle_key(message: Message, key: str) -> bool:
    if not key.isnumeric():
        return False

    user_id = redis.get(f"tg_key:{key}")

    if not user_id:
        return False

    await db.execute(
        "UPDATE users SET telegram_id = $2 WHERE id = $1;",
        int(user_id),
        int(message.from_user.id),
    )
    return True


class Form(StatesGroup):
    key = State()


@dp.message(CommandStart(deep_link=True))
async def command_start_handler(
    message: Message, command: CommandObject, state: FSMContext
) -> None:
    await state.set_state(Form.key)

    success = await handle_key(message, command.args)

    if success:
        await state.clear()
        await message.answer("Your account is successfully connected!")
    else:
        await state.set_state(Form.key)
        await message.answer("Invalid key. Please, try again:")


@form_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.key)
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!\nWhat is your key?"
    )


@form_router.message(Form.key)
async def process_key(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)

    if await handle_key(message, message.text):
        await state.clear()
        await message.answer("Your account is successfully connected!")
    else:
        await state.set_state(Form.key)
        await message.answer("Invalid key. Please, try again:")
        pass


async def main() -> None:
    global redis, db
    redis = Redis(
        host=settings.redis_host, port=settings.redis_port, decode_responses=True
    )
    db = await asyncpg.connect(
        f"postgresql://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}/postgres"
    )

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
