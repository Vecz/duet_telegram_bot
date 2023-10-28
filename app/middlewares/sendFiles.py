from app.models import db, DBfunc, Filefunc
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from app.keys import make_keyboard, load_message
from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender
dbFunc = DBfunc()
fFunc = Filefunc()

# Это будет outer-мидлварь на любые колбэки
class FileCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        locale = await dbFunc.get(event.from_user.id)
        locale = locale.locale
        new_file = await fFunc.check_new()
        if new_file != None:
            msg = await load_message(locale, "new_video")
            await event.answer(
                msg,
                show_alert=True)
            while 1:
                new_file = await fFunc.check_new()
                if(new_file):
                    await fFunc.update("file_id", new_file.name, 2)
                else:
                    break


        return await handler(event, data)

        