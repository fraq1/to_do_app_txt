from aiogram.types import Message
from aiogram import BaseMiddleware
from UI_tg_bot.Keyboards.Start_keyboard import get_main_keyboard

class RequireDateMiddleware(BaseMiddleware):
    _REQUIRED_COMMANDS = {
        "✏️ Write new note",
        "📝 Edit note text",
        "⏰ Edit note time",
        "🗑️ Delete note"
    }

    async def __call__(self, handler, event, data):
        cache = data["cache"]
        user_id = event.from_user.id
        day_date = cache.get(user_id, "date")

        if hasattr(event, "text") and event.text in self._REQUIRED_COMMANDS:
            if day_date is None:
                await event.answer(
                    "📅 Choose a date first.",
                    reply_markup=get_main_keyboard()
                )
                return

        if day_date is not None:
            data["day_date"] = day_date

        return await handler(event, data)