import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis
import logging
import os
from config.config import TOKEN, REDIS_HOST, REDIS_PORT, REDIS_POOL_SIZE, REDIS_DB
from app.handlers.main_menu import router as mm_router
from app.handlers.bot_settings import router as bs_router
from app.handlers.status import router as st_router
from app.handlers.root import router as root_router
from app.handlers.list_of_videos import router as lof_router
from app.handlers.sftp import router as sftp_router
from app.handlers.printer_control import router as pc_router
from app.models import DBfunc, init_db, db
from app.camera import capture
from app.middlewares.sendFiles import FileCallbackMiddleware
bot = Bot(token=TOKEN)
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    #os.system("docker-compose up -d")
    storage = Redis()
    dp = Dispatcher(storage=RedisStorage(storage))
    await init_db()
    #router
    dp.include_router(pc_router)
    dp.include_router(sftp_router)
    dp.include_router(lof_router)
    dp.include_router(root_router)
    dp.include_router(st_router)
    dp.include_router(bs_router)
    dp.include_router(mm_router)

    #middleware
    dp.callback_query.outer_middleware(FileCallbackMiddleware())
    dp.message.outer_middleware(FileCallbackMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Create tasks
    capture_task = loop.create_task(capture(bot))
    main_task = loop.create_task(main())

    # Run tasks
    
    
    loop.run_until_complete(asyncio.gather(main_task, capture_task))