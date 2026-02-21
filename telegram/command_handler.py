from aiogram import Router
from aiogram.filters import Command
import red

command_router = Router()

@command_router.message(Command("reset"))
async def reset(message):
    await red.clear_history(message.from_user.id)
    await message.answer("История очищена")