import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute(
        'CREATE TABLE IF NOT EXISTS orders(name TEXT, pizza_name TEXT, pizza_size TEXT, address TEXT, phone TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:  # открываем наш словарь
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        start_price = int(float(ret[-1]))
        prices = {25: start_price, 30: start_price + 5, 35: start_price + 10, 40: start_price + 15}

        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦены:\n'
                                                           f'Маленькая: {prices[25]}\nСредняя: {prices[30]}\nБольшая: {prices[35]}\nКоролевская: {prices[40]}')


async def sql_read3(message):
    orders = cur.execute('SELECT * FROM orders').fetchall()
    for order in orders:
        await bot.send_message(message.from_user.id,
                               f"Name {order[0]}\nPizza name {order[1]}\nsize {order[2]}\naddress {order[3]}\nphone {order[4]} ")


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()


async def sql_add_order(state):
    async with state.proxy() as data:  # открываем наш словарь
        cur.execute('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()
