from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiofiles

import json


async def make_keyboard(locale: str = 'EN', part = "main_menu") -> InlineKeyboardMarkup:
    async with aiofiles.open(f"locale/{locale}.json", encoding='utf-8') as f:
        file = await f.read()
    buttons = json.loads(file)['buttons'][part]
    val = list(buttons.values())
    key = list(buttons.keys())
    btn = [[InlineKeyboardButton(text=val[i], callback_data=key[i])] for i in range(len(buttons))]
    return InlineKeyboardBuilder(btn).as_markup()



async def load_message(locale: str = "EN", *args) -> str:
    async with aiofiles.open(f"locale/{locale}.json", encoding='utf-8') as f:
        file = await f.read()
    messages = json.loads(file)['messages']
    ans = ''
    for i in args:
        ans += messages[i]
    return ans
