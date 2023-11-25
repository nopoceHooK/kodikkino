from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton

random_btn = KeyboardButton('Случайные фильмы')
search_btn = KeyboardButton('Поиск')
adv_search_btn = KeyboardButton('Поиск с фильтрами')

categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

categories_kb.add(random_btn, search_btn, adv_search_btn)