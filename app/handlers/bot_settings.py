from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.models import DBfunc, db
from app.keys import make_keyboard, load_message
from app.states import CameraStates
from os import listdir
router = Router()
dbFunc = DBfunc()


@router.callback_query(F.data == "settings")
async def settings_menu(callback: types.CallbackQuery, state: FSMContext):
    #print(callback)
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    keyboard = await make_keyboard(locale, "settings")
    messages = await load_message(locale, "settings")
    await callback.message.edit_text(
        text=messages,
        reply_markup=keyboard
    )
    await state.set_state(CameraStates.Settings)
    await callback.answer()


@router.callback_query(CameraStates.Settings, F.data == "lang")
async def settings_menu(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    keyboard = await make_keyboard(locale, "lang")
    messages = await load_message(locale, "lang")
    for i in listdir("locale"):
        messages+= i.split(".")[0] + "\n"
    await callback.message.edit_text(
        text=messages,
        reply_markup=keyboard
    )
    await state.set_state(CameraStates.Locale)
    await callback.answer()

@router.message(CameraStates.Locale, F.text.len() == 2)
async def settings_menu(message: Message, state: FSMContext):
    locale = message.text
    dbFunc.update("locale", message.from_user.id, locale)
    keyboard = await make_keyboard(locale, "lang")
    messages = await load_message(locale, "value_changed")
    await message.reply(text=messages, reply_markup= keyboard)
    await state.set_state(CameraStates.Locale)

