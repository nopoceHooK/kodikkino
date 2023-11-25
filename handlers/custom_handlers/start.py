from aiogram import types
from loader import dp


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	"""
	Хендлер для обработки команды /start
	"""
	await message.answer('Привет! Для начала работы с ботом открой меню и выбери комманду или введи /help для '
											 'получения списка комманд.')
