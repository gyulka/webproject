from vkbottle import API
import asyncio
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
import os
import random
import requests
from typing import Optional
import config
from config import db_server_api
from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
from vkbottle.bot import Bot, Message

token = "b2ac558da42dc23e631f34d3b5795ed6dbf8bd647001a703b8aa70f79bed894556abf4ee1b0fd7568626d"

bot = Bot(token=token)

# -----клавиатуры
keyboard_hello = Keyboard(one_time=True).add(Text("Начать", {"cmd": "start"})).get_json()

keyboard_main = (Keyboard(one_time=False).add(Text("Купить", {"cmd": "aio"}))
                 .add(Text("Помочь", {"cmd": "aio"}))
                 .row()
                 .add(Text("Профиль", {"cmd": "aio"}))
                 .add(Text("Перевести", {"cmd": "aio"}))).get_json()

keyboard_buy = (Keyboard(one_time=False)
                .add(Text("1 разработчик", {"cmd": "puy"}))
                .row()
                .add(Text("Команда из 3х", {"cmd": "puy"}))
                .row()
                .add(Text("Команда из 5ти", {"cmd": "puy"}))
                .row()
                .add(Text("Небольшая студия из 10", {"cmd": "puy"}))
                .row()
                .add(Text("Крупная студия 30 человек", {"cmd": "puy"}))
                .row()
                .add(Text("Меню", {"cmd": "puy"}))).get_json()

keyboard_user = (Keyboard(one_time=False)
                 .add(Text("Сменить ник", {"cmd": "user"}))
                 .row()
                 .add(Text("Меню", {"cmd": "user"}))).get_json()

keyboard_help = (Keyboard(one_time=False)
                 .add(Text("Меню", {"cmd": "help"}))).get_json()


# -----клавиатуры


def shablon1():
    a, b = 0, 1000
    x = f"({random.randint(-b, b)} {random.choice(['*', '-', '+', '/'])} {random.randint(a, b)}) {random.choice(['*', '-', '+', '/'])} ({random.randint(-b, b)} {random.choice(['*', '-', '+', '/'])} {random.randint(a, b)})"
    return x, eval(x)


async def gen_primer(user_id, message):
    shablon = random.choice([shablon1])
    text, ans = shablon()
    ans = round(ans, 2)
    requests.post(db_server_api + 'set_helping', params={
        'vk': True,
        'id': user_id,
        'helping': str(ans)
    })
    requests.post(db_server_api + 'set_menu', params={
        'vk': True,
        'id': user_id,
        'menu': config.HELPING
    })
    print(ans)
    await message.answer('Решите\n' + text + '\nчтобы прекратить, нажмите на любую кнопку')


@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}".format(users_info[0].first_name), keyboard=keyboard_hello)


@bot.on.message(text=["/start <item>", "/start", 'Начать', '!start'])
@bot.on.message(payload={"cmd": "start"})
async def eat_handler(message: Message, item: Optional[str] = None):
    print(message)
    user_info = await bot.api.users.get(message.from_id)
    user_id = user_info[0].id
    user_name = user_info[0].first_name + ' ' + user_info[0].last_name
    print(user_id)
    response = requests.post(db_server_api + 'add_user', params={
        'id': user_id,
        'nick': user_name,
        'vk': 'True'
    })
    print(123)
    await message.answer(
        "Добро пожаловать в симулятор тим менеджера! \n Здесь вам требуется нанимать команды разработчиков, каждый час в 00 минут вы будете получать деньги на свой баланс в зависимости от того, сколько у вас команд\nРаз в 3 дня проводится конкурс проектов, так что чем больше у вас команд, тем выше у вас шанс победить!",
        keyboard=keyboard_main)


@bot.on.message(text=["/main <item>", "/main"])
@bot.on.message(payload={"cmd": "aio"})
async def eat_handler(message: Message, item: Optional[str] = None):
    user_info = await bot.api.users.get(message.from_id)
    user_id = user_info[0].id
    response = requests.get(config.db_server_api + 'get_user', params={
        'id': user_id,
        'vk': True
    }).json()
    txt = message.text.split()[-1]
    if txt == 'Помочь':
        await message.answer(f"Помощь в пути", keyboard=keyboard_help)
    elif txt == 'Купить':
        await message.answer(f"Выберите из списка:", keyboard=keyboard_buy)
    elif txt == 'Профиль':
        text = f'''ник: {response['nick']}
        уникальный id: {user_id}_1
        баланс: {response['score']}
        крупных студий: {response['count5']}
        мелких студий: {response['count4']}
        больших команд: {response['count3']}
        средних команд: {response['count2']}
        одиночных разработчиков: {response['count1']}
        общая производительность: {config.perfomance1 * response['count1'] + config.perfomance2 * response['count2'] + config.perfomance3 * response['count3'] + config.perfomance4 * response['count4'] + config.perfomance5 * response['count5']}/час'''

        await message.answer(text, keyboard=keyboard_user)
    elif txt == 'Перевести':
        requests.post(config.db_server_api + 'set_menu', params={
            'id': user_id,
            'vk': True,
            'menu': config.TRANSFER
        })
        await message.answer('введите сумму и id куда перевести ввиде')
        await message.answer('!go сумма id')
    elif response['menu'] == config.TRANSFER:
        summ, id = message.text.split()
        response = requests.post(config.db_server_api + 'transfer', params={
            'vk': True,
            'id': user_id,
            'score': summ,
            'id_to': id
        }).json()
        if response['succes']:
            await message.answer(f'успешно переведено {summ} {response["nick_to"]}')
            requests.post(db_server_api + 'set_menu', params={
                'vk': True,
                'id': user_id,
                'menu': 0
            })
            requests.post(db_server_api + 'set_menu', params={
                'vk': True,
                'id': user_id,
                'menu': config.MAIN
            })

        else:
            print(response['error'])
    elif response['menu'] == config.HELPING:
        if message.text == response['helping']:
            requests.post(db_server_api + 'add_score', params={
                'vk': True,
                'id': user_id,
                'score': 10
            })
            await message.answer('вам добавили 1')
            await gen_primer(user_id, message)
        else:
            await message.answer('неверный ответ\nдля нового примера, нажмите на кнопку второй раз')
    elif response['menu'] == config.CHANGE:
        nick = message.text
        requests.post(db_server_api + 'set_nick', params={
            'vk': True,
            'id': user_id,
            'nick': nick
        })
        requests.post(db_server_api + 'set_menu', params={
            'vk': True,
            'id': user_id,
            'menu': config.MAIN
        })
        await message.answer(f'ник успешно изменён на {message.text}', keyboard=keyboard_main)

@bot.on.message(text='!go <summ> <id>')
async def transfer(message: Message, summ: int, id: str):
    user_info = await bot.api.users.get(message.from_id)
    user_id = user_info[0].id
    response = requests.post(config.db_server_api + 'transfer', params={
        'vk': True,
        'id': user_id,
        'score': summ,
        'id_to': id
    }).json()
    if response['succes']:
        await message.answer(f'успешно переведено {summ} {response["nick_to"]}')
        requests.post(db_server_api + 'set_menu', params={
            'vk': True,
            'id': user_id,
            'menu': 0
        })
        requests.post(db_server_api + 'set_menu', params={
            'vk': True,
            'id': user_id,
            'menu': config.MAIN
        })

    else:
        print(response['error'])



@bot.on.message(text=["/help <item>", "/help"])
@bot.on.message(payload={"cmd": "help"})
async def eat_handler(message: Message, item: Optional[str] = None):
    user_info = await bot.api.users.get(message.from_id)
    user_id = user_info[0].id
    response = requests.get(config.db_server_api + 'get_user', params={
        'id': user_id,
        'vk': True
    }).json()
    if message.text == response['helping']:
        requests.post(db_server_api + 'add_score', params={
            'vk': True,
            'id': user_id,
            'score': 10
        })
        await message.answer('вам добавили 1')
        await gen_primer(user_id, message)
    else:
        await message.answer('неверный ответ\nдля нового примера, нажмите на кнопку второй раз')



@bot.on.message(text=["/puy <item>"])
@bot.on.message(payload={"cmd": 'puy'})
async def eat_handler(message: Message, item: Optional[str] = None):
    if item is None:
        txt = message.text.split()
        print(txt[0])
        if txt[0] == '[club194932267|@club194932267]':
            txt = txt[1:]
            print(txt)
        print(txt)
        item = ' '.join(txt)
    await message.answer(f"Купил {item}", keyboard=keyboard_main)


@bot.on.message(text=["/user <item>"])
@bot.on.message(payload={"cmd": 'user'})
async def change(message: Message, item: Optional[str] = None):
    if item is None:
        nick = message.text
    else:
        nick = item
    user_info = await bot.api.users.get(message.from_id)
    user_id = user_info[0].id
    requests.post(db_server_api + 'set_nick', params={
        'vk': True,
        'id': user_id,
        'nick': nick
    })
    requests.post(db_server_api + 'set_menu', params={
        'vk': True,
        'id': user_id,
        'menu': config.MAIN
    })
    await message.answer(f'ник успешно изменён на {message.text}', keyboard=keyboard_main)



@bot.on.message(text="Доброе утро")
async def good_morning(message: Message):
    await message.answer('Утро добрым не бывает. Утро')


@bot.on.message(text=["Утро", "утро"])
async def morning(message: Message):
    await message.answer('Утро')


@bot.on.message()
async def hi(message: Message):
    print(message)
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Честно говоря, я тебя не понял")


bot.run_forever()
