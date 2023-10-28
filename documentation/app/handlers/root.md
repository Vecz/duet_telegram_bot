## Documentation for `root.py`

### File Description

`root.py` contains handlers for managing root access and changing IP addresses.

### Imports

- `from aiogram import F, Router, types`: Importing necessary classes and functions from the `aiogram` library for working with the Telegram API.

- `from aiogram.fsm.context import FSMContext`: Importing the Finite State Machine (FSM) context for managing user states.

- `from app.models import DBfunc, db`: Importing functions for working with the database.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from app.states import CameraStates`: Importing states of the finite state machine.

- `from app.middlewares.is_root import RootCallbackMiddleware`: Importing a middleware for checking root access.

### Setting up Middlewares

```python
router.callback_query.middleware(RootCallbackMiddleware())
router.message.middleware(RootCallbackMiddleware())
```
Setting up the `RootCallbackMiddleware` middleware for handling root access.

### Handler root
```python
@router.callback_query(F.data == "root")
async def root(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Root"` button is pressed.

### Handler changeRoot
```python
@router.callback_query(CameraStates.Root, F.data == "become_root" or F.data == "leave_root")
async def changeRoot(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Become Root"` or `"Leave Root"` buttons are pressed.

### Handler changeIP
```python
@router.callback_query(CameraStates.Root, F.data.startswith("ip"))
async def changeIP(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when an `IP change` option is selected.

### Handler camera and printer
```python
@router.message(CameraStates.IpCamera, F.text)
async def camera(message: types.Message, state: FSMContext):
    # ... code handling ...

@router.message(CameraStates.IpPrinter, F.text)
async def camera(message: types.Message, state: FSMContext):
    # ... code handling ...
```
These handlers are triggered when a camera or printer IP is provided for update.