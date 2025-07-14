from aiogram import Router, types
from aiogram.filters import CommandObject, Command
from config import OPENAI_API_KEY, FREE_LIMIT
import openai

router = Router()
user_limits = {}

@router.message(Command("ai"))
async def ai_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id not in user_limits:
        user_limits[user_id] = 0
    if user_limits[user_id] >= FREE_LIMIT:
        await message.answer("❗ Лимит бесплатных AI-ответов исчерпан! Чтобы продолжить, оформите подписку.")
        return

    prompt = command.args
    if not prompt:
        await message.answer("✍️ После команды /ai напишите свой вопрос, например: /ai Как заработать миллион?")
        return

    await message.answer("🤖 Думаю...")

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        reply = response.choices[0].message.content.strip()
        user_limits[user_id] += 1
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"Ошибка AI: {e}")

def register_handlers(dp):
    dp.include_router(router)