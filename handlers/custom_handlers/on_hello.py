from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler()
async def hello_replier(message: types.Message, state: FSMContext):
	"""
	Хендлер для обработки сообщений от пользователя
	"""
	if message.text.lower() in ['привет', 'здравствуйте', 'прив', 'добрый день', 'добрый вечер']:
		await message.answer_sticker(r'CAACAgIAAxkBAAK5aWTWT6ZcBXvoP1C6wbRiLTMNhAbbAAL_EAAClzRAS6QnUKReEydIMAQ')
		await message.answer(
			f'Привет, {message.from_user.first_name}👋! Для начала работы с ботом открой меню и выбери команду или введи /help для получения списка команд.')
		await state.set_state()
	else:
		await message.answer_sticker(r'CAACAgIAAxkBAAK5c2TWUtTcRTRgKxbuWvZrSK3-HHiwAALkEgACOHUAAUoE0LZNVG4hoDAE')
		await message.answer(
			'Не понимаю вас. Для начала работы с ботом пожалуйста откройте меню и выберите команду или введите /help для получения списка комманд.')
		await state.set_state()
