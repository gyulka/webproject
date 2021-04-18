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
keyboard_hello = Keyboard(one_time=False).add(Text("Начать", {"cmd": "start"})).get_json()

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


@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}".format(users_info[0].first_name))


@bot.on.message(text=["/start <item>", "/start"])
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
        user_info = await bot.api.users.get(message.from_id)
        user_id = user_info[0].id
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
        user_info = await bot.api.users.get(message.from_id)
        user_id = user_info[0].id
        requests.post(config.db_server_api + 'set_menu', params={
            'id': user_id,
            'vk': True,
            'menu': config.TRANFER
        })
        await message.answer(f"Недоступно")


@bot.on.message(text=["/help <item>", "/help"])
@bot.on.message(payload={"cmd": "help"})
async def eat_handler(message: Message, item: Optional[str] = None):
    await message.answer('введите сумму и id куда перевести через пробел', keyboard=keyboard_main)


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
async def eat_handler(message: Message, item: Optional[str] = None):
    if item is None:
        txt = message.text.split()
        print(txt[0])
    await message.answer(f"ну ок", keyboard=keyboard_main)


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
