## Documentation for `list_of_videos.py`

### File Description

`list_of_videos.py` contains handlers for managing and displaying a list of videos.

### Imports

- `from aiogram import F, Router, types, flags`: Importing necessary classes and functions from the `aiogram` library for working with the Telegram API.

- `from aiogram.fsm.context import FSMContext`: Importing the Finite State Machine (FSM) context for managing user states.

- `from app.models import DBfunc, db, Filefunc`: Importing functions for working with the database and managing files.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from app.states import CameraStates`: Importing states of the finite state machine.

- `from aiogram.types import InlineKeyboardButton`: Importing types for inline keyboard buttons.

- `from aiogram.utils.keyboard import InlineKeyboardBuilder`: Importing a utility for building inline keyboards.

- `from aiogram.types import FSInputFile`: Importing a type for file uploads.

- `from config.config import VIDEO_DIR, STR_PER_PAGES`: Importing constants for video directory and pagination.

- `from app.middlewares.uploud import UploadCallbackMiddleware`: Importing a middleware for handling file uploads.

### Creating a Router

```python
router = Router()
router = Router()
```
Creating a `Router` object for handling requests.

### Initializing Functions and Objects
```python
dbFunc = DBfunc()
fFunc = Filefunc()
```
Initializing objects for working with the database and files.

### Middleware
```python
router.callback_query.middleware(UploadCallbackMiddleware())
```
Adding the `UploadCallbackMiddleware`  as a middleware for callback queries.

### Callback Handler list
```python
@router.callback_query(F.data == "list_of_videos")
async def list(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This callback handler is triggered when the `"List of Videos"` button is pressed in the main menu.

- `callback`: Callback query object.

- `state`: Finite State Machine context for managing user states.

### Callback Handler load
```python
@router.callback_query(CameraStates.ListOfVideos, F.data.isdigit(), flags={'chat_action': 'video_upload'})
async def load(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This callback handler is triggered when a video is selected from the list.

- `callback`: Callback query object.

- `state`: Finite State Machine context for managing user states.

### Callback Handler page
```python
@router.callback_query(CameraStates.ListOfVideos,F.data.startswith("page"))
async def page(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This callback handler is triggered when the user requests to paginate through the list of videos.

- `callback`: Callback query object.

- `state`: Finite State Machine context for managing user states.

### General Comments
- The code uses asynchronous functions to efficiently handle multiple requests simultaneously.

- Each handler is provided with a brief description, specifying input parameters and the logic of operation.

- Pagination logic is implemented to display a limited number of videos per page.