import random

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import config
from config import db_server_api, TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# -----клавиатуры
keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(KeyboardButton('купить'), KeyboardButton('помочь'), )
keyboard_main.add(KeyboardButton('профиль'), KeyboardButton('перевести'), )

keyboard_buy = InlineKeyboardMarkup(resize_keyboard=True)
keyboard_buy.add(InlineKeyboardButton('1 разработчик', callback_data='buy_1'))
keyboard_buy.add(InlineKeyboardButton('команда из 3', callback_data='buy_2'))
keyboard_buy.add(InlineKeyboardButton('команда из 5', callback_data='buy_3'))
keyboard_buy.add(InlineKeyboardButton('небольшая студия из 10', callback_data='buy_4'))
keyboard_buy.add(InlineKeyboardButton('крупная студия 30 человек', callback_data='buy_5'))

keyboard_user = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_user.add(KeyboardButton('сменить ник'))
keyboard_user.add(KeyboardButton('назад'))


# ---------------


def shablon1():
    a, b = 0, 1000
    x = f"({random.randint(-b, b)} {random.choice(['*', '-', '+', '/'])} {random.randint(a, b)}) {random.choice(['*', '-', '+', '/'])} ({random.randint(-b, b)} {random.choice(['*', '-', '+', '/'])} {random.randint(a, b)})"
    return x, eval(x)


async def gen_primer(message):
    shablon = random.choice([shablon1])
    text, ans = shablon()
    ans = round(ans, 2)
    requests.post(db_server_api + 'set_helping', params={
        'vk': False,
        'id': message.from_user.id,
        'helping': str(ans)
    })
    requests.post(db_server_api + 'set_menu', params={
        'vk': False,
        'id': message.from_user.id,
        'menu': config.HELPING
    })
    print(ans)
    await message.answer('Решите\n' + text + '\nчтобы прекратить, нажмите на любую кнопку')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    nick = message.from_user.username
    response = requests.post(db_server_api + 'add_user', params={
        'id': user_id,
        'nick': nick,
        'vk': 'False'
    })
    await message.reply(
        "Добро пожаловать в симулятор тим менеджера!\n Здесь вам требуется нанимать команды разработчиков, каждый час в 00 минут вы будете получать деньги на свой баланс в зависимости от того, сколько у вас команд\nРаз в 3 дня проводится конкурс проектов, так что чем больше у вас команд, тем выше у вас шанс победить!",
        reply_markup=keyboard_main)


@dp.message_handler()
async def messages(message: types.Message):
    response = requests.get(config.db_server_api + 'get_user', params={
        'id': message.from_user.id,
        'vk': False
    }).json()
    if message.text == 'купить':
        await message.answer(f'''выберите из списка баланс - {response['score']}:
1 разработчик {config.perfomance1}/час :{round(config.price1 * (1.1 ** response['count1']))}
команда из 3 {config.perfomance1}/час :{round(config.price2 * (1.1 ** response['count2']))}
команда из 5 {config.perfomance1}/час :{round(config.price3 * (1.1 ** response['count3']))}
небольшая студия из 10 {config.perfomance1}/час :{round(config.price4 * (1.1 ** response['count4']))}
крупная студия 30 человек {config.perfomance1}/час :{round(config.price5 * (1.1 ** response['count5']))}
''', reply_markup=keyboard_buy)
    elif message.text == 'профиль':
        text = f'''ник: {response['nick']}
уникальный id: {message.from_user.id}_0
баланс: {response['score']}
крупных студий: {response['count5']}
мелких студий: {response['count4']}
больших команд: {response['count3']}
средних команд: {response['count2']}
одиночных разработчиков: {response['count1']}
общая производительность: {config.perfomance1 * response['count1'] + config.perfomance2 * response['count2'] + config.perfomance3 * response['count3'] + config.perfomance4 * response['count4'] + config.perfomance5 * response['count5']}/час'''
        await message.answer(text, reply_markup=keyboard_user)
    elif message.text == 'перевести':
        requests.post(config.db_server_api + 'set_menu', params={
            'id': message.from_user.id,
            'vk': False,
            'menu': config.TRANSFER
        })
        await message.answer('введите сумму и id куда перевести через пробел')
    elif message.text == 'помочь':
        await gen_primer(message)
    elif message.text == 'назад':
        await send_welcome(message)
    elif message.text == 'сменить ник':
        requests.post(db_server_api + 'set_menu', params={
            'id': message.from_user.id,
            'vk': False,
            'menu': config.CHANGE
        })
        await message.answer('введите желаемый ник')


    elif response['menu'] == config.TRANSFER:
        summ, id = message.text.split()
        response = requests.post(config.db_server_api + 'transfer', params={
            'vk': False,
            'id': message.from_user.id,
            'score': summ,
            'id_to': id
        }).json()
        if response['success']:
            await message.answer(f'успешно переведено {summ} {response["nick_to"]}')
            requests.post(db_server_api + 'set_menu', params={
                'vk': False,
                'id': message.from_user.id,
                'menu': 0
            })
            requests.post(db_server_api + 'set_menu', params={
                'vk': False,
                'id': message.from_user.id,
                'menu': config.MAIN
            })

        elif response['error'] == 'not enough money':
            await message.answer(f'не хватает денег')
        else:
            print(response['error'])
    elif response['menu'] == config.HELPING:
        if message.text == response['helping']:
            requests.post(db_server_api + 'add_score', params={
                'vk': False,
                'id': message.from_user.id,
                'score': 10
            })
            await message.answer('вам добавили 10')
            await gen_primer(message)
        else:
            await message.answer('неверный ответ\nдля нового примера, нажмите на кнопку второй раз')
    elif response['menu'] == config.CHANGE:
        nick = message.text
        requests.post(db_server_api + 'set_nick', params={
            'vk': False,
            'id': message.from_user.id,
            'nick': nick
        })
        requests.post(db_server_api + 'set_menu', params={
            'vk': False,
            'id': message.from_user.id,
            'menu': config.MAIN
        })
        await message.answer(f'ник успешно изменён на {message.text}', reply_markup=keyboard_main)


@dp.callback_query_handler()
async def call_back(callback: types.CallbackQuery):
    resrponse = requests.post(config.db_server_api + callback.data, params={
        'id': callback.from_user.id,
        'vk': False
    })
    if resrponse.json()['success']:
        await callback.message.edit_text('успешно куплено')
    else:
        await callback.message.edit_text('не хватает денег')


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
