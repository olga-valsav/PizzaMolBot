from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # ,ReplyKeyboardRemove

b1 = KeyboardButton('🕰Режим работы')
b2 = KeyboardButton('📟Расположение')
b3 = KeyboardButton('🍕Меню')
b6 = KeyboardButton('🍽Создать заказ')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(b3, b6).row(b1, b2)

s1 = KeyboardButton('Маленькая')
s2 = KeyboardButton('Средняя')
s3 = KeyboardButton('Большая')
s4 = KeyboardButton('Королевская')
kb_size = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_size.row(s1, s2).row(s3, s4)
