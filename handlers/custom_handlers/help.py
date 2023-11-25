from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(commands=['help'])
async def hello_replier(message: types.Message):
	"""
	Хендлер для обработки команды /start
	"""
	await message.answer('Вот список команд доступных на данный момент:\n'
											 '/help - информация о командах\n'
											 '/search - простой поиск фильма по названию\n'
											 '/adv_search - поиск фильма по фильтрам\n'
											 '/random - получить случайный фильм из базы\n')
