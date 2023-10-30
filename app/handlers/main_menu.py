from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.models import DBfunc, db
from app.keys import make_keyboard, load_message
from app.states import CameraStates
router = Router()
dbFunc = DBfunc()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await dbFunc.add(message.from_user.id, message.chat.id)
    locale = await dbFunc.get(message.from_user.id)
    locale = locale.locale
    keyboard = await make_keyboard(locale, "main_menu")
    messages = await load_message(locale, "main_menu")
    await message.answer(
        text=messages,
        reply_markup=keyboard,
    )
    await state.set_state(CameraStates.MainMenu)


@router.callback_query(F.data == "main_menu")
async def cmd_back(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    keyboard = await make_keyboard(locale, "main_menu")
    messages = await load_message(locale, "main_menu")
    try:
        await callback.message.edit_text(
            text=messages,
            reply_markup=keyboard
        )
    except:
        await callback.message.answer(
            text=messages,
            reply_markup=keyboard
        )
    await state.set_state(CameraStates.MainMenu)
    await callback.answer()

