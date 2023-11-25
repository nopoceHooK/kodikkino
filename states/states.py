from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
	"""
	Состояния для хендлера search
	"""
	search_name = State()


class SearchData(StatesGroup):
	"""
	Состояния для хендлера adv_search
	"""
	year = State()
	genre = State()
	country = State()
	name = State()

class SearchHistory(StatesGroup):
	"""
	Состояния для хендлера history
	"""
	category = State()