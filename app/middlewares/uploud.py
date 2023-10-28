from app.models import db, DBfunc, Filefunc
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from app.keys import make_keyboard, load_message
from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender
from config.config import TOKEN
dbFunc = DBfunc()
fFunc = Filefunc()

# Это будет outer-мидлварь на любые колбэки
class UploadCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        flg = get_flag(data, "chat_action")
        if not flg:
            return await handler(event, data)
        elif flg == 'video_upload':
            async with ChatActionSender.upload_video(chat_id=event.message.chat.id, bot = Bot(token = TOKEN)):
                return await handler(event, data)
        else:
            async with ChatActionSender.upload_document(chat_id=event.chat.id, bot = Bot(token = TOKEN)):
                return await handler(event, data)

        