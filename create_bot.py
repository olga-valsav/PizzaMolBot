from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
#запускаем классы
storage = MemoryStorage()
token = os.getenv('PZ_TOKEN')
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
