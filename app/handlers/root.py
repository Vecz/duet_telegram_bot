from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from app.models import DBfunc, db
from app.keys import make_keyboard, load_message
from app.states import CameraStates
from app.middlewares.is_root import RootCallbackMiddleware
router = Router()
dbFunc = DBfunc()
router.callback_query.middleware(RootCallbackMiddleware())
router.message.middleware(RootCallbackMiddleware())


@router.callback_query(F.data == "root")
async def root(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    if root:
        key = "root"
    else:
        key = "root_warning"
    keyboard = await make_keyboard(locale, key)
    messages = await load_message(locale, key)
    await callback.message.edit_text(
        text= messages,
        reply_markup= keyboard
    )
    await state.set_state(CameraStates.Root)
    await callback.answer()

@router.callback_query(CameraStates.Root, F.data == "become_root" or F.data == "leave_root")
async def changeRoot(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    if root:
        key = "root_warning"
        await dbFunc.update("root", root.user_id, 0)
    else:
        key = "root"
        await dbFunc.update("root", callback.from_user.id, 1)
    keyboard = await make_keyboard(locale, key)
    messages = await load_message(locale, "value_changed",key)
    await callback.message.edit_text(
        text= messages,
        reply_markup= keyboard
    )
    await callback.answer()

@router.callback_query(CameraStates.Root, F.data.startswith("ip"))
async def changeIP(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    if(callback.data == "ip_printer"):
        await state.set_state(CameraStates.IpPrinter)
    else:
        await state.set_state(CameraStates.IpCamera)
    keyboard = await make_keyboard(locale, "change_ip")
    messages = await load_message(locale, "change_ip")
    await callback.message.edit_text(
        text= messages,
        reply_markup= keyboard
    )
    await callback.answer()


@router.message(CameraStates.IpCamera, F.text)
async def camera(message: types.Message, state: FSMContext):
    locale = await dbFunc.get(message.from_user.id)
    locale = locale.locale
    data = {
        "url": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    if(data["url"][-1] == '/'):
        data["url"] = data["url"][:-1]
    await dbFunc.update("camera_ip", message.from_user.id, data["url"])
    keyboard = await make_keyboard(locale, "change_ip")
    messages = await load_message(locale, "camera","ip","value_changed","change_ip")
    messages = messages.format(data['url'])
    await message.reply(
        text= messages,
        reply_markup=keyboard
    )

@router.message(CameraStates.IpPrinter, F.text)
async def camera(message: types.Message, state: FSMContext):
    locale = await dbFunc.get(message.from_user.id)
    locale = locale.locale
    data = {
        "url": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    if(data["url"][-1] == '/'):
        data["url"] = data["url"][:-1]
    await dbFunc.update("printer_ip", message.from_user.id, data["url"])
    keyboard = await make_keyboard(locale, "change_ip")
    messages = await load_message(locale, "printer","ip","value_changed","change_ip")
    messages = messages.format(data['url'])
    await message.reply(
        text= messages,
        reply_markup=keyboard
    )