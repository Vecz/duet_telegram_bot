## Documentation for `printer_control.py`

### File Description

`printer_control.py` contains handlers for controlling the printer, running macros, and sending G-code commands.

### Imports

- `from aiogram import F, Router, types`: Importing necessary classes and functions from the `aiogram` library for working with the Telegram API.

- `from aiogram.fsm.context import FSMContext`: Importing the Finite State Machine (FSM) context for managing user states.

- `from app.models import DBfunc, db`: Importing functions for working with the database.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from app.states import CameraStates`: Importing states of the finite state machine.

- `from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton`: Importing types related to inline keyboards.

- `from aiogram.utils.keyboard import InlineKeyboardBuilder`: Importing a utility for building inline keyboards.

- `from app.middlewares.is_root import RootCallbackMiddleware`: Importing a middleware for checking root access.

- `from config.config import STR_PER_PAGES`: Importing a constant for pagination.

- `import aiohttp`: Importing an asynchronous HTTP client.

### Setting up Middlewares

```python
router.callback_query.middleware(RootCallbackMiddleware())
router.callback_query.outer_middleware(RootCallbackMiddleware())
router.message.middleware(RootCallbackMiddleware())
router.message.outer_middleware(RootCallbackMiddleware())
```
Setting up the RootCallbackMiddleware middleware for handling root access.

### Handler printer_control
```python
@router.callback_query(F.data == "printer_control")
async def printer_control(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Printer Control"` button is pressed.

### Handler run_macros
```python
@router.callback_query(F.data == "run_macros", CameraStates.PrinterControl)
async def run_macros(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Run Macros"` button is pressed in the printer control menu.

### Handler page
```python
@router.callback_query(CameraStates.RunMacros,F.data.startswith("page"))
async def page(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when navigating between pages in the macros list.

###  Handler macros
```python
@router.callback_query(F.data.isdigit(), CameraStates.RunMacros)
async def macros(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when a specific macro is selected from the list.

### Handler wait_gcode
```python
@router.callback_query(CameraStates.PrinterControl, F.data == "send_gcode")
async def wait_gcode(callback: types.CallbackQuery, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when the `"Send G-code"` button is pressed.

### Handler send_gcode
```python
@router.message(CameraStates.SendGcode)
async def send_gcode(message: types.Message, state: FSMContext):
    # ... code handling ...
```
This handler is triggered when a `G-code` command is sent.
