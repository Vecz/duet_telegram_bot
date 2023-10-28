from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from app.models import DBfunc, db
from app.keys import make_keyboard, load_message
from app.states import CameraStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.middlewares.is_root import RootCallbackMiddleware
from config.config import STR_PER_PAGES
import aiohttp
router = Router()
dbFunc = DBfunc()
router.callback_query.middleware(RootCallbackMiddleware())
router.callback_query.outer_middleware(RootCallbackMiddleware())
router.message.middleware(RootCallbackMiddleware())
router.message.outer_middleware(RootCallbackMiddleware())

@router.callback_query(F.data == "printer_control")
async def printer_control(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    messages = await load_message(locale, "printer_control")
    keyboard = await make_keyboard(locale, "printer_control")
    await callback.message.edit_text(
        text=messages,
        reply_markup=keyboard
    )
    await state.set_state(CameraStates.PrinterControl)
    await callback.answer()

@router.callback_query(F.data == "run_macros", CameraStates.PrinterControl)
async def run_macros(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    printer_url = root.printer_ip
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(printer_url+"/rr_connect?password=") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_files?dir=/macros/") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
                r = await resp.json()
                r = r['files']
            btn = [[InlineKeyboardButton(text=r[i], callback_data=str(i))] for i in range(len(r))]
            messages = await load_message(locale, "printer_control")
            back = await load_message(locale, "back")
            if(len(btn) > STR_PER_PAGES):
                btn = btn[:STR_PER_PAGES]
                next = await load_message(locale, "next")
                btn.append([InlineKeyboardButton(text=back, callback_data="printer_control"),InlineKeyboardButton(text=next, callback_data="page_1")])
            elif len(btn) > 0:
                btn.append([InlineKeyboardButton(text=back, callback_data="printer_control")])
            keyboard = InlineKeyboardBuilder(btn).as_markup()
            await state.set_state(CameraStates.RunMacros)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "printer_control")
    await callback.message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    await callback.answer()

@router.callback_query(CameraStates.RunMacros,F.data.startswith("page"))
async def page(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    cur_page = int(callback.data.split('_')[1])
    messages = await load_message(locale, "printer_control")
    messages += str(cur_page)
    next = await load_message(locale, "next")
    back = await load_message(locale, "back")
    root = await dbFunc.get_root()
    printer_url = root.printer_ip
    next_callback = f"page_{cur_page+1}"
    if cur_page - 1 > 0:
        back_callback = f"page_{cur_page-1}"
    else:
        back_callback = "printer_control"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(printer_url+"/rr_connect?password=") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_files?dir=/macros/") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
                r = await resp.json()
                r = r['files']
            btn = [[InlineKeyboardButton(text=r[i], callback_data=str(i))] for i in range(len(r))]
            btn = btn[STR_PER_PAGES*cur_page:]
            messages = await load_message(locale, "printer_control")
            back = await load_message(locale, "back")
            if(len(btn) > STR_PER_PAGES):
                btn = btn[:STR_PER_PAGES]
                btn.append([InlineKeyboardButton(text=back, callback_data=back_callback),InlineKeyboardButton(text=next, callback_data=next_callback)])
            elif len(btn) > 0:
                btn.append([InlineKeyboardButton(text=back, callback_data=back_callback)])
            keyboard = InlineKeyboardBuilder(btn).as_markup()
            await state.set_state(CameraStates.RunMacros)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "printer_control")
    await callback.message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    await callback.answer()


@router.callback_query(F.data.isdigit(), CameraStates.RunMacros)
async def macros(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    printer_url = root.printer_ip
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(printer_url+"/rr_connect?password=") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_files?dir=/macros/") as resp:
                r = await resp.json()
                filename = r['files'][int(callback.data)]
            async with session.get(printer_url+"/rr_gcode?gcode=M32 /macros/"+filename) as resp:
                r = await resp.json()
            messages = await load_message(locale, "run_macros", "success", "printer_control")
            keyboard = await make_keyboard(locale, "printer_control")
            
            await state.set_state(CameraStates.PrinterControl)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "printer_control")
    await callback.message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    
    await callback.answer()

@router.callback_query(CameraStates.PrinterControl, F.data == "send_gcode")
async def wait_gcode(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    await state.set_state(CameraStates.SendGcode)
    messages = await load_message(locale, "send_gcode")
    keyboard = await make_keyboard(locale, "send_gcode")
    await callback.message.edit_text(
        text= messages,
        reply_markup= keyboard
    )
    await callback.answer()

@router.message(CameraStates.SendGcode)
async def send_gcode(message: types.Message, state: FSMContext):
    locale = await dbFunc.get(message.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    printer_url = root.printer_ip
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(printer_url+"/rr_connect?password=") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+f"/rr_gcode?gcode={message.text}") as resp:
                r = await resp.json()
            messages = await load_message(locale, "run_macros", "success", "printer_control")
            messages+=str(r)
            keyboard = await make_keyboard(locale, "printer_control")
            
            await state.set_state(CameraStates.PrinterControl)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "printer_control")
    await message.answer(
        text= messages,
        reply_markup= keyboard
    )