from aiogram import BaseMiddleware

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if event.text == "/start":
            return await handler(event, data)
        logic = data["logic"]
        user_id = logic.find_user_id(event.from_user.id)
        if not user_id:
            await event.answer(
                "Please type /start to begin.",
            )
            return
        return await handler(event, data)