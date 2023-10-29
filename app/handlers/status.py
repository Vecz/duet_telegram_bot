from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile, InputMediaPhoto
from app.models import DBfunc, db
from app.keys import make_keyboard, load_message
from app.states import CameraStates
from aiogram.utils.callback_answer import CallbackAnswer
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
import aiohttp
router = Router()
dbFunc = DBfunc()
router.callback_query.middleware(CallbackAnswerMiddleware(pre=False, text="Готово!", show_alert=False))
@router.callback_query(CameraStates.LastShot, F.data == "refresh")
async def lastShot(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    keyboard = await make_keyboard(locale, "last_shot")
    img_url = f"{root.camera_ip}/shot.jpg"
    await callback.message.edit_media(
        media = InputMediaPhoto(media = URLInputFile(img_url)),  
        reply_markup= keyboard
    )
    await state.set_state(CameraStates.LastShot)
    await callback.answer()

@router.callback_query(CameraStates.Status, F.data == "cancel")
async def lastShot(callback: types.CallbackQuery, state: FSMContext, callback_answer: CallbackAnswer):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    if root == None:
        msg = await load_message(locale, "root_warning")
        callback_answer.text = msg
        callback_answer.show_alert = True
    elif callback.from_user.id == root.user_id:
        ...
    else:
        msg = await load_message(locale, "not_root")
        callback_answer.text = msg
        callback_answer.show_alert = True
        return
    keyboard = await make_keyboard(locale, "status")
    messages = await load_message(locale, "cancel","status")
    printer_url = root.printer_ip
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(printer_url+"/rr_gcode?gcode=M25") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_gcode?gcode=M0") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
    except Exception as e:
        messages = e.args + messages
    await callback.message.edit_text(
            text=messages,
            reply_markup=keyboard
        )
    await state.set_state(CameraStates.Status)
    await callback.answer()


@router.callback_query(CameraStates.Status, F.data == "last_shot")
async def lastShot(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    keyboard = await make_keyboard(locale, "last_shot")
    messages = await load_message(locale, "last_shot")
    img_url = f"{root.camera_ip}/shot.jpg"
    await callback.message.answer_photo(
        URLInputFile(img_url),
        caption= messages,
        reply_markup= keyboard
    )
    await state.set_state(CameraStates.LastShot)
    await callback.answer()

@router.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    if root != None:
        printer_url = root.printer_ip
        camera_url = root.camera_ip
        keyboard = await make_keyboard(locale, "status")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(printer_url+"/rr_connect?password=") as resp:
                    if resp.status != 200:
                        msg = await load_message(locale, "connect_fail")
                        raise Exception(msg)
                async with session.get(printer_url+"/rr_model?key=state") as resp:
                    if resp.status != 200:
                        msg = await load_message(locale, "connect_fail")
                        raise Exception(msg)
                    r = await resp.json()
                    r = r['result']
                
                val = r["status"]
                t = await load_message(locale, "status")
                t = t.format(val)
                async with session.get(printer_url+"/rr_model?key=heat") as resp:
                    if resp.status != 200:
                        msg = await load_message(locale, "connect_fail")
                        raise Exception(msg)
                    r = await resp.json()
                    r = r['result']
                j = 0 
                for i in r['heaters']:
                    t+= await load_message(locale, "heater")
                    t = t.format(j,i['current'] )
                    j+=1
                if val == "processing":
                    async with session.get(printer_url+"/rr_model?key=job") as resp:
                        if resp.status != 200:
                            msg = await load_message(locale, "connect_fail")
                            raise Exception(msg)
                        r = await resp.json()
                        #print(r)
                        r = r['result']
                        sec = int(r["timesLeft"]["slicer"])
                        t+= await load_message(locale, "percent", "name", "estimated")
                        t = t.format(float(r['filePosition']) / float(r['file']['size']) * 100, r['file']['fileName'],
                                    sec//3600, (sec//60)%60 ,sec % 60)
                messages = t
        except Exception as e:
            print(e.args)
            messages = str(e.args)
        try:
            print(messages)
            await callback.message.edit_text(
                text=messages,
                reply_markup=keyboard
            )
        except:
            await callback.message.answer(
                text=messages,
                reply_markup=keyboard
            )
        await state.set_state(CameraStates.Status)
    else:
        keyboard = await make_keyboard(locale, "main_menu")
        messages = await load_message(locale, "setup_need", "main_menu")
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
