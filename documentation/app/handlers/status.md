## Documentation for `status.py`

### File Description

`status.py` contains handlers for displaying printer and camera status, as well as handling actions related to these statuses.

### Imports

- `from aiogram import F, Router, types`: Importing necessary classes and functions from the `aiogram` library for working with the Telegram API.

- `from aiogram.filters import Command`: Importing the `Command` filter for handling bot commands.

- `from aiogram.fsm.context import FSMContext`: Importing the Finite State Machine (FSM) context for managing user states.

- `from aiogram.types import Message, BufferedInputFile, URLInputFile, InputMediaPhoto`: Importing types for working with messages and media.

- `from app.models import DBfunc, db`: Importing functions for working with the database.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from app.states import CameraStates`: Importing states of the finite state machine.

- `import aiohttp`: Importing the aiohttp library for making asynchronous HTTP requests.

- `from PIL import Image, ImageFile`: Importing classes for working with images.

### Initializing Router and DB Functions

```python
router = Router()
dbFunc = DBfunc()
```
Creating an instance of the `Router` for handling routes and an instance of `DBfunc` for database functions.

### Handler lastShot
```python
@router.callback_query(CameraStates.LastShot, F.data == "refresh")
async def lastShot(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Refresh"` button is pressed to get the last camera shot.

### Handler lastShot (continued)
```python
@router.callback_query(CameraStates.Status, F.data == "last_shot")
async def lastShot(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Last Shot"` button is pressed to view the last camera shot.

### Handler status
```python
@router.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Status"` button is pressed to view `printer` and `camera` status.

### Handler lastShot (continued)
```python
@router.callback_query(CameraStates.Status, F.data == "cancel")
async def lastShot(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the user `cancels` an action related to status.