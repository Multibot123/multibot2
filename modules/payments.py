from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("pay"))
async def pay_handler(message: types.Message):
    await message.answer("Payments модуль включён! (оплата подключается позже)")

def register_handlers(dp):
    dp.include_router(router)