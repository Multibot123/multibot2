from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("archive"))
async def archive_handler(message: types.Message):
    await message.answer("Archive модуль готов! (архив добавим позже)")

def register_handlers(dp):
    dp.include_router(router)