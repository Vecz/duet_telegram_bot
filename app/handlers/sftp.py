from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from app.models import DBfunc, db
from app.keys import make_keyboard, load_message
from app.states import CameraStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
from config.config import TOKEN, STR_PER_PAGES
from app.middlewares.uploud import UploadCallbackMiddleware
from app.middlewares.is_root import RootCallbackMiddleware
router = Router()
dbFunc = DBfunc()
router.message.middleware(UploadCallbackMiddleware())
router.message.outer_middleware(UploadCallbackMiddleware())
router.callback_query.middleware(RootCallbackMiddleware())
router.callback_query.outer_middleware(RootCallbackMiddleware())


@router.callback_query(F.data == "sftp")
async def sftp(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    root = await dbFunc.get_root()
    if root == None or root.user_id == callback.from_user.id:
        keyboard = await make_keyboard(locale, "sftp")
        messages = await load_message(locale, 'sftp')
        await callback.message.edit_text(
            text=messages,  
            reply_markup= keyboard
        )
        await state.set_state(CameraStates.SendFilesToPrint)
    else:
        keyboard = await make_keyboard(locale, "main_menu")
        messages = await load_message(locale, "not_root", "main_menu")
        await callback.message.edit_text(
            text=messages,  
            reply_markup= keyboard
        )
    await callback.answer()

@router.callback_query(F.data == "from_storage", CameraStates.SendFilesToPrint)
async def from_storage(callback: types.CallbackQuery, state: FSMContext):
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
            async with session.get(printer_url+"/rr_files?dir=/gcodes/") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
                r = await resp.json()
                r = r['files']
            btn = [[InlineKeyboardButton(text=r[i], callback_data=str(i))] for i in range(len(r))]
            msg = await load_message(locale, "sftp")
            back = await load_message(locale, "back")
            if(len(btn) > STR_PER_PAGES):
                btn = btn[:STR_PER_PAGES]
                next = await load_message(locale, "next")
                btn.append([InlineKeyboardButton(text=back, callback_data="sftp"),InlineKeyboardButton(text=next, callback_data="page_1")])
            elif len(btn) > 0:
                btn.append([InlineKeyboardButton(text=back, callback_data="sftp")])
            keyboard = InlineKeyboardBuilder(btn).as_markup()
            messages = await load_message(locale, "from_storage")
            await state.set_state(CameraStates.FromStorage)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "sftp")
    await callback.message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    
    await callback.answer()



@router.callback_query(CameraStates.FromStorage,F.data.startswith("page"))
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
        back_callback = "sftp"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(printer_url+"/rr_connect?password=") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_files?dir=/gcodes/") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
                r = await resp.json()
                r = r['files']
            btn = [[InlineKeyboardButton(text=r[i], callback_data=str(i))] for i in range(len(r))]
            btn = btn[STR_PER_PAGES*cur_page:]
            messages = await load_message(locale, "sftp")
            back = await load_message(locale, "back")
            if(len(btn) > STR_PER_PAGES):
                btn = btn[:STR_PER_PAGES]
                btn.append([InlineKeyboardButton(text=back, callback_data=back_callback),InlineKeyboardButton(text=next, callback_data=next_callback)])
            elif len(btn) > 0:
                btn.append([InlineKeyboardButton(text=back, callback_data=back_callback)])
            keyboard = InlineKeyboardBuilder(btn).as_markup()
            await state.set_state(CameraStates.SendFilesToPrint)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "sftp")
    await callback.message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    await callback.answer()


@router.callback_query(F.data.isdigit(), CameraStates.FromStorage)
async def print(callback: types.CallbackQuery, state: FSMContext):
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
            async with session.get(printer_url+"/rr_files?dir=/gcodes/") as resp:
                r = await resp.json()
                filename = r['files'][int(callback.data)]
            async with session.get(printer_url+"/rr_gcode?gcode=M32 /gcodes/"+filename) as resp:
                r = await resp.json()
            messages = await load_message(locale, "from_storage", "success", "main_menu")
            keyboard = await make_keyboard(locale, "main_menu")
            
            await state.set_state(CameraStates.MainMenu)
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "sftp")
    await callback.message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    
    await callback.answer()  


@router.callback_query(CameraStates.SendFilesToPrint, F.data.startswith("from"))
async def from_url_or_file(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    if(callback.data == "from_url"):
        await state.set_state(CameraStates.FromUrl)
        messages = await load_message(locale, "from_url")
    else:
        await state.set_state(CameraStates.FromFile)
        messages = await load_message(locale, "from_file")
    keyboard = await make_keyboard(locale, "load_file")
    await callback.message.edit_text(
        text= messages,
        reply_markup= keyboard
    )
    await callback.answer()


@router.message(CameraStates.FromUrl, F.text, flags={'chat_action': 'file_upload'})
async def from_url(message: types.Message, state: FSMContext):
    locale = await dbFunc.get(message.from_user.id)
    locale = locale.locale
    data = {
        "url": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    
    messages = await load_message(locale, "success", "from_url", "loading")
    messages = messages.format(data['url'])
    message = await message.reply(
        text= messages
    )
    root = await dbFunc.get_root()
    printer_url = root.printer_ip
    filename = "gcodes/"+data["url"].split("/")[-1]
    url = data["url"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(data["url"]) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(filename, 'wb') as file:
                        file.write(content)
                else:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_connect?password=") as resp:
                if resp.status != 200:
                    msg = await load_message(locale, "connect_fail")
                    raise Exception(msg)
            with open(filename, 'rb') as file:
                data = aiohttp.FormData()
                data.add_field('file', file, filename=filename)
            async with session.post(printer_url+f"/rr_upload?name=/{filename}", data=data) as response:
                if response.status == 200:
                    msg = f'Error uploading file: HTTP status {response.status}'
                    raise Exception(msg)
            async with session.get(printer_url+"/rr_gcode?gcode=M32 /"+filename) as resp:
                r = await resp.json()
            messages = await load_message(locale, "from_url", "success", "main_menu")
            keyboard = await make_keyboard(locale, "main_menu")
    except Exception as e:
        messages = str(e.args)
        keyboard = await make_keyboard(locale, "sftp")
    await message.edit_text(
        text=messages,  
        reply_markup= keyboard
    )
    await state.set_state(CameraStates.MainMenu)


@router.message(CameraStates.FromFile, flags={'chat_action': 'file_upload'})
async def from_file(message: types.Message, state: FSMContext):
    locale = await dbFunc.get(message.from_user.id)
    locale = locale.locale
    if message.document.file_id:
        document = message.document 
        messages = await load_message(locale, "success", "from_file", "loading")
        message = await message.answer(
            text= messages
        )
        root = await dbFunc.get_root()
        printer_url = root.printer_ip
        filename = "gcodes/"+ document.file_name
        bot = Bot(token = TOKEN)
        await bot.download(
            document,
            destination=filename
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(printer_url+"/rr_connect?password=") as resp:
                    if resp.status != 200:
                        msg = await load_message(locale, "connect_fail")
                        raise Exception(msg)
                with open(filename, 'rb') as file:
                    data = aiohttp.FormData()
                    data.add_field('file', file, filename=filename)
                    async with session.post(printer_url+f"/rr_upload?name=/{filename}", data=data) as response:
                        if response.status != 200:
                            msg = f'Error uploading file: HTTP status {response.status}'
                            raise Exception(msg)
                async with session.get(printer_url+"/rr_gcode?gcode=M32 /"+filename) as resp:
                    r = await resp.json()
                messages = await load_message(locale, "from_file", "success", "main_menu")
                keyboard = await make_keyboard(locale, "main_menu")
        except Exception as e:
            messages = str(e.args)
            keyboard = await make_keyboard(locale, "sftp")
        await message.edit_text(
            text=messages,  
            reply_markup= keyboard
        )
    else:
        messages = await load_message(locale, "error", "from_file", "loading", "main_menu")
        keyboard = await make_keyboard(locale, "main_menu")
        message = await message.reply(
            text= messages,
            reply_markup=keyboard
        )

    
    await state.set_state(CameraStates.MainMenu)
