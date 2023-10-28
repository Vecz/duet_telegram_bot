## Documentation for `main.py`

### File Description

`main.py` is the main entry point of the application. It initializes the bot, sets up the necessary components, and starts polling for updates.

### Imports

- `asyncio`: Asynchronous programming library for Python.
- `aiogram`: A high-level framework for building Telegram bots.
- `RedisStorage`, `FSMStrategy`: Components for handling Finite State Machines (FSM) using Redis as storage.
- `Redis`: Redis client for asyncio.
- `logging`: Python's built-in logging module.
- `os`: Provides a portable way of interacting with the operating system.
- `config.config`: Module containing application configuration variables.
- Various router modules and handlers from the `app` directory.
- `DBfunc`, `init_db`, `db`: Database-related components from `app.models`.

### Variables

- `bot`: An instance of the `Bot` class, representing the Telegram bot.
- `storage`: An instance of the Redis client for managing storage.
- `dp`: An instance of the `Dispatcher` class, responsible for handling updates and routing them to the appropriate handlers.

### Function `main()`

```python
async def main():
    # ... code ...
```
This is the main function that sets up the bot and dispatches updates.

- Initializes logging configuration.

- Initializes the Redis storage.

- Creates an instance of the Dispatcher with Redis storage.

- Initializes the database.

- Includes various routers using dp.include_router().

- Sets up the FileCallbackMiddleware as outer middleware for both callback queries and messages.

- Starts polling for updates.

### Block if __name__ == "__main__":
This block is executed when the script is run directly.

- Creates an event loop.

- Creates tasks for capture() and main().

- Runs the tasks concurrently using asyncio.gather().