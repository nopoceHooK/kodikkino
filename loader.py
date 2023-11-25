from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_data.config import TELEGRAM_BOT_KEY

bot = Bot(token=TELEGRAM_BOT_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())

