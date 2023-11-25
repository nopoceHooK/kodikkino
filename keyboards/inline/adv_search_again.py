from aiogram import types

keyboard = types.InlineKeyboardMarkup()
button = types.InlineKeyboardButton(text='Повторить поиск', callback_data='adv_re_search')
keyboard.add(button)
