import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import config
from config import db_server_api, TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# -----клавиатуры
keyboard_main = ReplyKeyboardMarkup()
keyboard_main.add(KeyboardButton('купить'), KeyboardButton('помочь'), )
keyboard_main.add(KeyboardButton('профиль'), KeyboardButton('перевести'), )

keyboard_buy = InlineKeyboardMarkup()
keyboard_buy.add(InlineKeyboardButton('1 разработчик', callback_data='buy_1'))
keyboard_buy.add(InlineKeyboardButton('команда из 3', callback_data='buy_2'))
keyboard_buy.add(InlineKeyboardButton('команда из 5', callback_data='buy_3'))
keyboard_buy.add(InlineKeyboardButton('небольшая студия из 10', callback_data='buy_4'))
keyboard_buy.add(InlineKeyboardButton('крупная студия 30 человек', callback_data='buy_5'))

keyboard_user = ReplyKeyboardMarkup()
keyboard_user.add(KeyboardButton('сменить ник'))


# ---------------
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
        await message.answer('выберите из списка:', reply_markup=keyboard_buy)
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
            'menu': config.TRANFER
        })
        await message.answer('введите сумму и id куда перевести через пробел')


    elif response['menu'] == config.TRANFER:
        summ, id = message.text.split()
        response = requests.post(config.db_server_api + 'tranfer', params={
            'vk': False,
            'id': message.from_user.id,
            'score': summ,
            'id_to': id
        }).json()
        if response['succes']:
            await message.answer(f'успешно переведено {summ} {response["nick_to"]}')


@dp.callback_query_handler()
async def call_back(callback: types.CallbackQuery):
    menu = requests.get(config.db_server_api + 'get_user', params={
        'id': callback.from_user.id,
        'vk': False
    }).json()
    print(menu)
    menu = menu['menu']

    resrponse = requests.post(config.db_server_api + callback.data, params={
        'id': callback.from_user.id,
        'vk': False
    })
    if resrponse.json()['succes']:
        await callback.message.edit_text('успешно куплено')
    else:
        await callback.message.edit_text('не хватает денег')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
