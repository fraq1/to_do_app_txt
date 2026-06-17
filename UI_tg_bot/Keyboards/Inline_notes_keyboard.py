from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from UI_tg_bot.Output_validators.normalize_output import normalize_time

def get_inline_notes_keyboard(notes):
    builder = InlineKeyboardBuilder()
    for i in notes:
        builder.button(text=f"{normalize_time(i.start_time)}-{normalize_time(i.end_time)} | {i.text}", callback_data=f"note:{i.note_id}")
    builder.adjust(1)
    return builder.as_markup()