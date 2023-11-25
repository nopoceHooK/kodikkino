from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton

fantasy_btn = KeyboardButton('Фэнтези')
scifi_btn = KeyboardButton('Фантастика')
horror_btn = KeyboardButton('Ужасы')
action_btn = KeyboardButton('Боевик')
comedy_btn = KeyboardButton('Комедия')
family_btn = KeyboardButton('Семейный')
anime_btn = KeyboardButton('Аниме')
drama_btn = KeyboardButton('Драма')

genres_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

genres_kb.add(fantasy_btn, scifi_btn, horror_btn, action_btn,
							comedy_btn, family_btn, anime_btn, drama_btn)
