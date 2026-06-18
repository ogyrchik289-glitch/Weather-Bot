from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from api_request import get_weather, get_weather_by_hours, get_weather_by_days
from keyboards.keyboards import start_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext  
from aiogram.filters import StateFilter
from datetime import datetime

handler_router = Router()

class Registration(StatesGroup):
    waiting_for_city = State()
    waiting_for_date = State()
    city_d = State()
    date_d = State()
    

@handler_router.message(F.tetx.contains("weather"))
async def get_weather_now(message: Message):
    data = message.text.split(" ")
    if len(data) == 1:
        await message.answer("Пожалуйста введите название грода после команды. Пример: '/weather Ташкент' ")
        return
    city = data[1]
    await message.answer(get_weather(city))

@handler_router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот для получения точной погоды по часам и дням. Выбери что интересует:", reply_markup=start_keyboard)
    
@handler_router.callback_query(F.data == "weather_by_h" )
async def weather_by_hours_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.waiting_for_city)
    await callback_query.message.answer("Введите город для получения погоды по часам:")
    
@handler_router.message(StateFilter(Registration.waiting_for_city))
async def get_city_h(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Registration.waiting_for_date)
    await message.answer("Введите дату в формате ГГГГ-ММ-ДД для получения погоды по часам:")
    
@handler_router.message(StateFilter(Registration.waiting_for_date))
async def get_date_h(message: Message, state: FSMContext):
        
    await state.update_data(date=message.text)
    data = await state.get_data()
    city = data.get("city")
    date = data.get("date")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД:")
        return
    
    await message.answer(get_weather_by_hours(city, date))
    await state.clear()
    
@handler_router.callback_query(F.data == "weather_by_d" )
async def weather_by_days_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.city_d)
    await callback_query.message.answer("Введите город для получения погоды:")
    
@handler_router.message(StateFilter(Registration.city_d))
async def get_city_d(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Registration.date_d)
    await message.answer("Введите дату в формате ГГГГ-ММ-ДД для получения погоды по часам:")
    
@handler_router.message(StateFilter(Registration.date_d))
async def get_date_d(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    city = data.get("city")
    date = data.get("date")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД:")
        return
    await message.answer(get_weather_by_days(city, date))
    await state.clear()
    
    
    
    