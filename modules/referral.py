from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("invite"))
async def invite_handler(message: types.Message):
    await message.answer("Referral система готова! (ссылка позже)")

def register_handlers(dp):
    dp.include_router(router)