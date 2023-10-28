## Documentation for `sftp.py`

### File Description

`sftp.py` contains handlers for managing SFTP functionality and file transfers.

### Imports

- `from aiogram import F, Router, types, Bot`: Importing necessary classes and functions from the `aiogram` library for working with the Telegram API.

- `from aiogram.fsm.context import FSMContext`: Importing the Finite State Machine (FSM) context for managing user states.

- `from app.models import DBfunc, db`: Importing functions for working with the database.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from app.states import CameraStates`: Importing states of the finite state machine.

- `from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton`: Importing classes for creating inline keyboards.

- `from aiogram.utils.keyboard import InlineKeyboardBuilder`: Importing utilities for working with inline keyboards.

- `import aiohttp`: Importing the aiohttp library for making asynchronous HTTP requests.

- `from config.config import TOKEN, STR_PER_PAGES`: Importing configuration parameters.

- `from app.middlewares.uploud import UploadCallbackMiddleware`: Importing middleware for handling file uploads.

- `from app.middlewares.is_root import RootCallbackMiddleware`: Importing middleware for checking root access.

### Setting up Middlewares

```python
router.message.middleware(UploadCallbackMiddleware())
router.message.outer_middleware(UploadCallbackMiddleware())
router.callback_query.middleware(RootCallbackMiddleware())
router.callback_query.outer_middleware(RootCallbackMiddleware())
```
Setting up the `UploadCallbackMiddleware` for handling file uploads and the `RootCallbackMiddleware` for handling root access.

### Handler sftp
```python
@router.callback_query(F.data == "sftp")
async def sftp(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"SFTP"` button is pressed.

### Handler from_storage
```python
@router.callback_query(F.data == "from_storage", CameraStates.SendFilesToPrint)
async def from_storage(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"From Storage"` button is pressed in the `SFTP` menu.

### Handler page
```python
@router.callback_query(CameraStates.FromStorage,F.data.startswith("page"))
async def page(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when a pagination button is pressed while browsing files.

### Handler print
```python
@router.callback_query(F.data.isdigit(), CameraStates.FromStorage)
async def print(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when a file is selected for printing.

### Handler from_url_or_file
```python
@router.callback_query(CameraStates.SendFilesToPrint, F.data.startswith("from"))
async def from_url_or_file(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the user chooses to send a file from a `URL` or from `their device`.

### Handler from_url
```python
@router.message(CameraStates.FromUrl, F.text, flags={'chat_action': 'file_upload'})
async def from_url(message: types.Message, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the user provides a `URL` for file upload.

### Handler from_file
```python
@router.message(CameraStates.FromFile, flags={'chat_action': 'file_upload'})
async def from_file(message: types.Message, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the user uploads a file from `their device`.