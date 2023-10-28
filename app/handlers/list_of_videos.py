from aiogram import F, Router, types, flags
from aiogram.fsm.context import FSMContext
from app.models import DBfunc, db, Filefunc
from app.keys import make_keyboard, load_message
from app.states import CameraStates
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from config.config import VIDEO_DIR, STR_PER_PAGES
from app.middlewares.uploud import UploadCallbackMiddleware
router = Router()
dbFunc = DBfunc()
fFunc = Filefunc()

router.callback_query.middleware(UploadCallbackMiddleware())

@router.callback_query(F.data == "list_of_videos")
async def list(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    messages = await load_message(locale, "list_of_videos")
    file_list = await fFunc.file_list()
    btn = [[InlineKeyboardButton(text=i.name, callback_data=str(i.id))] for i in file_list]
    back = await load_message(locale, "back")
    if(len(btn) > STR_PER_PAGES):
        btn = btn[:STR_PER_PAGES]
        next = await load_message(locale, "next")
        btn.append([InlineKeyboardButton(text=back, callback_data="main_menu"),InlineKeyboardButton(text=next, callback_data="page_1")])
    elif len(btn) > 0:
        btn.append([InlineKeyboardButton(text=back, callback_data="main_menu")])
    if(len(btn)!= 0):
        await callback.message.edit_text(
            text= messages,
            reply_markup= InlineKeyboardBuilder(btn).as_markup()
        )
        await state.set_state(CameraStates.ListOfVideos)
    else:
        messages = await load_message(locale, "error", "main_menu")
        keyboard = await make_keyboard(locale, "main_menu")
        await callback.message.edit_text(
            text= messages,
            reply_markup=keyboard
        )
    await callback.answer()


@router.callback_query(CameraStates.ListOfVideos, F.data.isdigit(), flags={'chat_action': 'video_upload'})
async def load(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    file = await fFunc.get_id(int(callback.data))
    key = await make_keyboard(locale,  "list_of_videos")
    if(file.file_id <= 3):
        video = FSInputFile(VIDEO_DIR+ file.name)
        msg = await callback.message.answer_video(
            video,
            caption=file.name,
            reply_markup=key
        )
        await fFunc.update(file.name, "file_id", msg.video.file_id)
    elif file.file_id > 3:
        await callback.message.answer_video(file.file_id, reply_markup=key)
    await state.set_state(CameraStates.MainMenu)
    await callback.answer()

@router.callback_query(CameraStates.ListOfVideos,F.data.startswith("page"))
async def page(callback: types.CallbackQuery, state: FSMContext):
    locale = await dbFunc.get(callback.from_user.id)
    locale = locale.locale
    cur_page = int(callback.data.split('_')[1])
    messages = await load_message(locale, "list_of_videos", "page")
    messages += str(cur_page)
    file_list = await fFunc.file_list()
    btn = [[InlineKeyboardButton(text=i.name, callback_data=str(i.id))] for i in file_list]
    next = await load_message(locale, "next")
    back = await load_message(locale, "back")
    next_callback = f"page_{cur_page+1}"
    if cur_page - 1 > 0:
        back_callback = f"page_{cur_page-1}"
    else:
        back_callback = "list_of_videos"
    btn = btn[STR_PER_PAGES*cur_page:]
    if(len(btn) > STR_PER_PAGES):
        btn = btn[:STR_PER_PAGES]
        btn.append([InlineKeyboardButton(text=back, callback_data=back_callback),
                    InlineKeyboardButton(text=next, callback_data=next_callback)])
    elif(len(btn) > 0):
        btn.append([InlineKeyboardButton(text=back, callback_data=back_callback)])
    if(len(btn)!= 0):
        await callback.message.edit_text(
            text= messages,
            reply_markup= InlineKeyboardBuilder(btn).as_markup()
        )
    else:
        messages = await load_message(locale, "error", "main_menu")
        keyboard = await make_keyboard(locale, "main_menu")
        await callback.message.edit_text(
            text= messages,
            reply_markup=keyboard
        )
        await state.set_state(CameraStates.MainMenu)
    await callback.answer()