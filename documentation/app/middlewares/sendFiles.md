## Documentation for `sendFiles.py`

### File Description

`sendFiles.py` contains a middleware class `FileCallbackMiddleware` that handles the sending of files and related actions.

### Imports

- `from app.models import db, DBfunc, Filefunc`: Importing the database, `DBfunc` and `Filefunc` classes for working with the database and files.

- `from typing import Callable, Dict, Any, Awaitable`: Importing necessary types for the middleware.

- `from aiogram import BaseMiddleware`: Importing the base middleware class for creating custom middlewares.

- `from aiogram.types import Message, CallbackQuery`: Importing message and callback query types for handling events.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from aiogram.dispatcher.flags import get_flag`: Importing a function for getting flags from the dispatcher.

- `from aiogram.utils.chat_action import ChatActionSender`: Importing a class for sending chat actions.

### Initializing `DBfunc` and `Filefunc`

```python
dbFunc = DBfunc()
fFunc = Filefunc()
```
Creating instances of the `DBfunc` and `Filefunc` classes for database and file functions, respectively.

### Class FileCallbackMiddleware
```python
class FileCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # ... code ...
```
This class extends the `BaseMiddleware` and overrides its __call__ method to implement custom middleware behavior.

### Middleware Function
```python
async def __call__(
    self,
    handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
    event: CallbackQuery,
    data: Dict[str, Any]
) -> Any:
    # ... code ...
```
The __call__ function is executed whenever a callback query event is received. It takes three arguments:

- `handler`: The handler function that will be called after the middleware processing.

- `event`: The callback query event.

- `data`: Additional data.

### Middleware Logic
```python
locale = await dbFunc.get(event.from_user.id)
locale = locale.locale
new_file = await fFunc.check_new()
if new_file != None:
    # ... code ...
```
- locale = await dbFunc.get(event.from_user.id): Gets the user's locale from the database.

- new_file = await fFunc.check_new(): Checks if there is a new file. If so, it shows a notification message.

- if new_file != None:: Checks if a new file is found.

- msg = await load_message(locale, "new_video"): Loads a message indicating a new video.

- await event.answer(msg, show_alert=True): Sends an alert message to the user.

- while 1:: Enters a loop to continuously check for new files.

- new_file = await fFunc.check_new(): Checks if there is a new file.

- if(new_file):: If a new file is found, it updates the file status and continues the loop.

- else:: If no new file is found, it breaks out of the loop.

### Returning the Result
```python
return await handler(event, data)
```
The result of the middleware processing is returned by calling the handler function with the event and data.