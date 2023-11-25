from aiogram import types


keyboard = types.InlineKeyboardMarkup()
button = types.InlineKeyboardButton(text='Очистить историю', callback_data='delete_history')
keyboard.add(button)
