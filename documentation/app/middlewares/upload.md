## Documentation for `upload.py`

### File Description

`upload.py` contains a middleware class `UploadCallbackMiddleware` that handles the uploading of files based on chat actions.

### Imports

- `from app.models import db, DBfunc, Filefunc`: Importing the database, `DBfunc` and `Filefunc` classes for working with the database and files.

- `from typing import Callable, Dict, Any, Awaitable`: Importing necessary types for the middleware.

- `from aiogram import BaseMiddleware, Bot`: Importing the base middleware class and the Bot class for creating custom middlewares and interacting with the Telegram bot API.

- `from aiogram.types import Message, CallbackQuery`: Importing message and callback query types for handling events.

- `from app.keys import make_keyboard, load_message`: Importing functions for creating keyboards and loading messages.

- `from aiogram.dispatcher.flags import get_flag`: Importing a function for getting flags from the dispatcher.

- `from aiogram.utils.chat_action import ChatActionSender`: Importing a class for sending chat actions.

- `from config.config import TOKEN`: Importing the bot token.

### Initializing `DBfunc` and `Filefunc`

```python
dbFunc = DBfunc()
fFunc = Filefunc()
```
Creating instances of the `DBfunc` and `Filefunc` classes for database and file functions, respectively.

### Class UploadCallbackMiddleware
```python
class UploadCallbackMiddleware(BaseMiddleware):
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

- handler: The handler function that will be called after the middleware processing.

- event: The callback query event.

- data: Additional data.

### Middleware Logic
```python
flg = get_flag(data, "chat_action")
if not flg:
    return await handler(event, data)
elif flg == 'video_upload':
    async with ChatActionSender.upload_video(chat_id=event.message.chat.id, bot = Bot(token = TOKEN)):
        return await handler(event, data)
else:
    async with ChatActionSender.upload_document(chat_id=event.message.chat.id, bot = Bot(token = TOKEN)):
        return await handler(event, data)
```
- flg = get_flag(data, "chat_action"): Gets the chat action flag from the dispatcher.

- if not flg:: Checks if there is no chat action flag. If so, it directly calls the handler.

- elif flg == 'video_upload':: Checks if the chat action flag indicates a video upload.

- async with ChatActionSender.upload_video(chat_id=event.message.chat.id, bot = Bot(token = TOKEN)):: Initiates the video upload action.

- else:: If the chat action flag is for document upload.

- async with ChatActionSender.upload_document(chat_id=event.message.chat.id, bot = Bot(token = TOKEN)):: Initiates the document upload action.

### Returning the Result
```python
return await handler(event, data)
```
The result of the middleware processing is returned by calling the handler function with the event and data.