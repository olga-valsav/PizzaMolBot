from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os



#запускаем классы
storage = MemoryStorage()
token = "6290649756:AAFc6Vf6jNaXR6s57S9Zd-LH3hYy97HglVE"
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
