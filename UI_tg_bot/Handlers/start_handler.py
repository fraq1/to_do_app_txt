from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from Business_logic.Business_logic import BusinessLogic
from UI_tg_bot.Keyboards.Start_keyboard import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, logic: BusinessLogic):
    logic.register_or_ignore_user(message.from_user.id, message.from_user.username)
    await message.answer("👋 Hello! I'm your personal daily planner.\n\nChoose a date to get started:", reply_markup=get_main_keyboard())