from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import timedelta


from Business_logic.Business_logic import BusinessLogic
from UI_tg_bot.Keyboards.Notes_keyboard import get_notes_keyboard, get_notes_short_keyboard
from Business_logic.LogicErrors import InputFormatError
from UI_tg_bot.Flows.Date_flow import DateFlowState
from UI_tg_bot.Output_validators.normalize_output import normalize_time, format_output
from UI_tg_bot.Cache.User_cache import UserCache

date_router = Router()

@date_router.message(F.text == "📅 Today")
async def today_date_handler(message:Message, logic: BusinessLogic, cache: UserCache):
    date = logic.return_today_date()
    notes = logic.chose_or_create_day(date, message.from_user.id)
    cache.set(message.from_user.id, "date", date)
    text = format_output(date, notes)
    if notes:
        await message.answer(text, reply_markup=get_notes_keyboard())
    else:
        await message.answer(text, reply_markup=get_notes_short_keyboard())

@date_router.message(F.text == "🌅 Tomorrow")
async def tomorrow_date_handler(message:Message, logic: BusinessLogic, cache: UserCache):
    date = logic.return_today_date()
    tomorrow = date + timedelta(days=1)
    notes = logic.chose_or_create_day(tomorrow, message.from_user.id)
    cache.set(message.from_user.id, "date", tomorrow)
    text = format_output(tomorrow, notes)
    if notes:
        await message.answer(text, reply_markup=get_notes_keyboard())
    else:
        await message.answer(text, reply_markup=get_notes_short_keyboard())


@date_router.message(F.text == "🗓 Enter date")
async def chose_date_handler(message: Message, state: FSMContext):
    await message.answer("📅 Enter the date in format YYYY MM DD:\nExample: 2024 01 15")
    await state.set_state(DateFlowState.waiting_for_input)

@date_router.message(DateFlowState.waiting_for_input)
async def input_handler(message:Message, state: FSMContext, logic: BusinessLogic, cache: UserCache):
    try:
        date = logic.validate_date(message.text)
    except InputFormatError as e:
        await message.answer(f"{e} Try again:")
        return

    notes = logic.chose_or_create_day(date, message.from_user.id)
    cache.set(message.from_user.id, "date", date)
    text = format_output(date, notes)
    if notes:
        await message.answer(text, reply_markup=get_notes_keyboard())
    else:
        await message.answer(text, reply_markup=get_notes_short_keyboard())
    await state.clear()
