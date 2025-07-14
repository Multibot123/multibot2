import json
import os

FILTERS_PATH = "data/user_filters.json"
if not os.path.exists("data"):
    os.mkdir("data")

def load_user_filters():
    if os.path.exists(FILTERS_PATH):
        with open(FILTERS_PATH, "r") as f:
            return {int(k): v for k, v in json.load(f).items()}
    return {}

def save_user_filters():
    with open(FILTERS_PATH, "w") as f:
        json.dump({str(k): v for k, v in user_filters.items()}, f)

user_filters = load_user_filters()   # <-- только ЭТА строка! не надо user_filters = {} ниже

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()
# user_filters = {}  # УДАЛИ или закомментируй! Всё грузится из load_user_filters()

DISTRICTS = ["Центральный", "САО", "ЮЗАО", "Белорусская", "Парк Культуры"]
BUDGETS = ["до 60 тыс", "до 90 тыс", "до 150 тыс"]

@router.message(Command("rent"))
async def start_rent(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=d)] for d in DISTRICTS],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Выберите район или метро:", reply_markup=kb)

@router.message(F.text.in_(DISTRICTS))
async def select_district(message: types.Message):
    user_id = message.from_user.id
    user_filters[user_id] = user_filters.get(user_id, {})
    user_filters[user_id]["district"] = message.text
    save_user_filters()  # <--- сохраняем после выбора района!

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b)] for b in BUDGETS],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Теперь выберите бюджет:", reply_markup=kb)

@router.message(F.text.in_(BUDGETS))
async def select_budget(message: types.Message):
    user_id = message.from_user.id
    user_filters[user_id] = user_filters.get(user_id, {})
    user_filters[user_id]["budget"] = message.text
    save_user_filters()  # <--- сохраняем после выбора бюджета!

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Сохранить фильтр")]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Нажмите 'Сохранить фильтр', чтобы получать алерты только по вашему запросу.", reply_markup=kb)

@router.message(F.text == "Сохранить фильтр")
async def save_filter(message: types.Message):
    user_id = message.from_user.id
    filt = user_filters.get(user_id, {})
    if "district" in filt and "budget" in filt:
        save_user_filters()  # <--- сохраняем фильтр перед подтверждением!
        await message.answer(f"✅ Фильтр сохранён: {filt['district']} / {filt['budget']}.\nТеперь вы будете получать только подходящие объявления!", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите район и бюджет сначала.")

def register_handlers(dp):
    dp.include_router(router)