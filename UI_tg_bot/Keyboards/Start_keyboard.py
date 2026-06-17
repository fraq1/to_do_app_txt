from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📅 Today")
    builder.button(text="🌅 Tomorrow")
    builder.button(text="🗓 Enter date")

    return builder.as_markup(resize_keyboard=True)