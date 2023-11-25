from aiogram import types


keyboard = types.InlineKeyboardMarkup()
button = types.InlineKeyboardButton(text='Найти другой!', callback_data='refresh')
keyboard.add(button)



