from app.models import db, DBfunc
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from app.keys import make_keyboard, load_message
dbFunc = DBfunc()

# Это будет outer-мидлварь на любые колбэки
class RootCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        locale = await dbFunc.get(event.from_user.id)
        locale = locale.locale
        root = await dbFunc.get_root()
        if root == None:
            msg = await load_message(locale, "root_warning")
            await event.answer(
                msg,
            show_alert=True
            )
            return await handler(event, data) 
        elif event.from_user.id == root.user_id:
            return await handler(event, data) 
        else:
            msg = await load_message(locale, "not_root")
            await event.answer(
                msg,
            show_alert=True
            )
            return