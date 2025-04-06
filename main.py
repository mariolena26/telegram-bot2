import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_TOKEN = "7535665268:AAFTBdOjciCRWNiDfLP0LSXDVon18JoJs38"
CHANNEL_ID = "-1002131435817"  # ID приватного каналу
CHANNEL_LINK = "https://t.me/+63phcsesEjZmNjBi"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

user_ages = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
    if chat_member.status not in ['member', 'creator', 'administrator']:
        await message.answer("Щоб продовжити, спочатку підпишіться на канал:
" + CHANNEL_LINK)
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Так", callback_data="age_yes"),
                 InlineKeyboardButton("Ні", callback_data="age_no"))
    await message.answer("На каналі контент 18+. Підтвердіть свій вік для вашої ж відповідальності:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ["age_yes", "age_no"])
async def process_age_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == "age_yes":
        user_ages[user_id] = True
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(user_id, f"Ласкаво просимо! Ось посилання на канал: {CHANNEL_LINK}")
    else:
        user_ages[user_id] = False
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(user_id, "Доступ заборонено.")

@dp.message_handler(commands=["age"])
async def change_age(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Так", callback_data="age_yes"),
                 InlineKeyboardButton("Ні", callback_data="age_no"))
    await message.answer("Підтвердіть свій вік ще раз:", reply_markup=keyboard)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
