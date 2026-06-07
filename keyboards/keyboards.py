from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram import Router

keyboard_router = Router()

btn_weather_by_hours = InlineKeyboardButton(text="Погода по часам", callback_data="weather_by_h")
btn_weather_by_days = InlineKeyboardButton(text="Погода по дням", callback_data="weather_by_d")

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [btn_weather_by_hours],
    [btn_weather_by_days]
])