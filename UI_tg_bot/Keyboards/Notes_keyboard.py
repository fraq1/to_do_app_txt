from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_notes_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="✏️ Write new note")
    builder.button(text="📝 Edit note text")
    builder.button(text="⏰ Edit note time")
    builder.button(text="🗑️ Delete note")
    builder.button(text="⬅️ Back")

    return builder.as_markup(resize_keyboard=True)

def get_notes_short_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="✏️ Write new note")
    builder.button(text="⬅️ Back")
    return builder.as_markup(resize_keyboard=True)