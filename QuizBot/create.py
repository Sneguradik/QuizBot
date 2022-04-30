import logging
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = '5215278600:AAGzxJ3cjN7fOy21ClxGLbYZ5__I4eSdixA'

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)