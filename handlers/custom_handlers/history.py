from loader import dp, bot
from database.database import User, Movies
from aiogram import types
from keyboards.reply.categories_btn import categories_kb
from states.states import SearchHistory
from aiogram.dispatcher import FSMContext
from keyboards.inline.delete_history import keyboard


@dp.message_handler(commands=['history'])
async def random_movie_command(message: types.Message):
	"""
	Хендлер обработки команды /history
	"""
	await SearchHistory.category.set()
	await message.answer('По какой категории показать историю?', reply_markup=categories_kb)


@dp.message_handler(state=SearchHistory.category)
async def random_movie_command(message: types.Message, state: FSMContext):
	"""
	Функция для поиска фильмов в бд с учетом id пользователя и категории поиска, выводящая ссылки на фильмы в ответном
	сообщении
	"""
	async with state.proxy() as data:
		data['category'] = message.text
		await state.finish()
		if data['category'] == 'Случайные фильмы':
			category = 'random'
			links = 'Рандом:\n'
		elif data['category'] == 'Поиск':
			category = 'search'
			links = 'Поиск:\n'
		elif data['category'] == 'Поиск с фильтрами':
			category = 'adv_search'
			links = 'Поиск с фильтрами:\n'
		else:
			await message.answer('Такой категории не существует.')
	user_id = message.from_user.id
	for movie in Movies.select().where(Movies.category == category, Movies.user == user_id):
		link = f'<a href="{movie.link}">{movie.movie_name}({movie.year})</a>'
		links += link + '\n'
	await message.answer(links, parse_mode='html', disable_web_page_preview=True, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'delete_history', state=None)
async def process_callback_button(callback_query: types.CallbackQuery):
	"""
	Хендлер обрабатывающий нажатие кнопки удаления истории
	"""
	callback_user_id = callback_query.from_user.id
	for movie in Movies.select().where(Movies.user == callback_user_id):
		movie.delete_instance()
	await bot.send_message(callback_query.from_user.id, 'История очищена!')
