import json
import os

ALERTS_PATH = "data/user_alerts.json"
if not os.path.exists("data"):
    os.mkdir("data")

def load_user_alerts():
    if os.path.exists(ALERTS_PATH):
        with open(ALERTS_PATH, "r") as f:
            return {int(k): set(v) for k, v in json.load(f).items()}
    return {}

def save_user_alerts():
    with open(ALERTS_PATH, "w") as f:
        json.dump({str(k): list(v) for k, v in user_alerts.items()}, f)

user_alerts = load_user_alerts()   # только эта строка! не создавай user_alerts = {} ниже

from modules import avito  # для поиска квартир на Авито
from modules import rent   # чтобы получить user_filters
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

router = Router()
bot = None  # сюда в main.py подкинешь объект Bot
ALERT_TOPICS = ["Аренда", "Курсы", "Крипта"]

@router.message(Command("alerts"))
async def alerts_menu(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=topic)] for topic in ALERT_TOPICS],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите тему для подписки на алерты:", reply_markup=kb)

@router.message(F.text.in_(ALERT_TOPICS))
async def subscribe_alert(message: types.Message):
    user_id = message.from_user.id
    topic = message.text
    if user_id not in user_alerts:
        user_alerts[user_id] = set()
    user_alerts[user_id].add(topic)
    save_user_alerts()   # сохраняем после изменения!
    await message.answer(f"Вы подписаны на алерты по теме: {topic}!\nТеперь вы будете получать уведомления по этой теме.", reply_markup=types.ReplyKeyboardRemove())

async def rent_alerts_main():
    print(f"user_alerts: {user_alerts}")
    print(f"user_filters: {rent.user_filters}")
    topic = "Аренда"
    for user_id, topics in user_alerts.items():
        print(f"Проверяем user_id: {user_id}, темы: {topics}")
        if topic in topics:
            user_filter = rent.user_filters.get(user_id)
            print(f"user_filter для {user_id}: {user_filter}")
            if not user_filter:
                continue
            district = user_filter.get("district", "")
            budget_str = user_filter.get("budget", "")
            try:
                budget_val = int("".join(filter(str.isdigit, budget_str))) * 1000
            except Exception:
                budget_val = 0

            print(f"Запрашиваем Avito: {district=}, {budget_val=}")
            flats = avito.search_avito_flats(district, budget_val)
            print(f"Найдено объявлений: {len(flats)}")
            if not flats:
                await bot.send_message(user_id, f"🔎 Пока нет объявлений по вашему фильтру: {district}, до {budget_val} руб.")
            else:
                for obj in flats:
                    text = f"🏢 {obj['title']}\n{obj['desc']}\nЦена: {obj['price']}₽\n{obj['link']}"
                    try:
                        await bot.send_message(user_id, text)
                    except Exception as e:
                        print(f"Ошибка алерта {user_id}: {e}")

def register_handlers(dp):
    dp.include_router(router)

async def rent_alert_scheduler():
    while True:
        await asyncio.sleep(60 * 20)  # каждые 20 минут (ставь своё значение)
        await rent_alerts_main()      # вызывай рассылку

@router.message(Command("send_rent_alert"))
async def manual_alert(message: types.Message):
    await rent_alerts_main()
    await message.answer("Алерты вручную отправлены!")