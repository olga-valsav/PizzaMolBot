from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки клавы админа
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
orders_list = KeyboardButton('/Просмотреть_заказы')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load) \
    .add(button_delete).add(orders_list)
