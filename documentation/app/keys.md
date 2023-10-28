## Documentation for `keys.py`

### File Description

`keys.py` is a module responsible for handling localization and creating inline keyboards.

### Imports

- `from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton`: Imports classes for working with inline keyboards.

- `from aiogram.utils.keyboard import InlineKeyboardBuilder`: Imports a utility for building inline keyboards.

- `import aiofiles`: A library for working with files asynchronously.

- `import json`: A library for working with JSON data.

### Function `make_keyboard(locale: str = 'EN', part = "main_menu")`

```python
async def make_keyboard(locale: str = 'EN', part = "main_menu") -> InlineKeyboardMarkup:
    # ... code ...
    return InlineKeyboardBuilder(btn).as_markup()
```
This function creates an inline keyboard based on the specified locale and part. It returns an `InlineKeyboardMarkup` object.

- locale: str = 'EN': Specifies the localization. Default is 'EN'.

- part = "main_menu": Specifies the part of the keyboard to be created. Default is "main_menu".

### Function load_message(locale: str = "EN", *args)
```python
async def load_message(locale: str = "EN", *args) -> str:
    # ... code ...
    return ans
```
This function loads messages based on the specified locale and arguments. It returns a string containing the concatenated messages.

- locale: str = "EN": Specifies the localization. Default is 'EN'.

- *args: Variable-length argument list for specifying message keys.