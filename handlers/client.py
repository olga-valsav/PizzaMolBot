from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import dp, bot
from keyboards.client_kb import kb_client, kb_size
from database import sqlite_db


class FSMClient(StatesGroup):
    name = State()
    pizza_name = State()
    size = State()
    address = State()
    phone = State()


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        await bot.send_message(message.from_user.id,
                               'Добро пожаловать! Хотите сделать заказ?',
                               reply_markup=kb_client)

    except:
        await message.reply('Ошибка')


async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00',
                           reply_markup=kb_client)


async def create_order(message: types.Message):
    await FSMClient.name.set()
    await message.reply('Вы начали создание заказа, введите команду "отмена" для отмены заказа.\nВведите свое имя:')


async def wait_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.next()
    await message.reply('Введите название пиццы')


async def wait_pizza_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pizza_name'] = message.text
    await FSMClient.next()
    await bot.send_message(message.from_user.id, 'Выберите размер пиццы', reply_markup=kb_size)


async def wait_pizza_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pizza_size'] = message.text
    await FSMClient.next()
    await message.reply("Напишите свой адрес")


async def wait_client_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['client_address'] = message.text
    await FSMClient.next()
    await message.reply("Напишите свой телефон")


async def wait_client_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['client_phone'] = message.text

    await sqlite_db.sql_add_order(state)
    await state.finish()  # команда завершает машино-состояние и все данные что мы получили выши нужно обработать
    await message.reply("Спасибо за заказ, оператор свяжется с Вами в ближайшее время!", reply_markup=kb_client)


async def cansel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Выполнено!', reply_markup=kb_client)


async def pizza_place_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15', reply_markup=kb_client)


async def pizza_menu_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Наше меню', reply_markup=kb_client)
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cansel_handler, Text(startswith='отмена', ignore_case=True), state='*')

    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(pizza_open_command, Text(startswith='🕰Режим работы'), state='*')
    dp.register_message_handler(pizza_place_command, Text(startswith='📟Расположение'), state='*')
    dp.register_message_handler(pizza_menu_command, Text(startswith='🍕Меню'), state='*')
    dp.register_message_handler(create_order, Text(startswith='🍽Создать заказ'), state=None)
    dp.register_message_handler(wait_client_name, state=FSMClient.name)
    dp.register_message_handler(wait_pizza_name, state=FSMClient.pizza_name)
    dp.register_message_handler(wait_pizza_size, state=FSMClient.size)
    dp.register_message_handler(wait_client_address, state=FSMClient.address)
    dp.register_message_handler(wait_client_phone, state=FSMClient.phone)
    dp.register_message_handler(cansel_handler, state='*', commands='отмена')
