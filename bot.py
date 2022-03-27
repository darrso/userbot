import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from config import api_id, api_hash

Client = Client('test', api_id, api_hash)

async def translator(text: 'str') -> str:
    russian = r'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    english = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>'
    russian_dict = {y: x for x, y in zip(russian, english)}
    english_dict = {x: y for x, y in zip(russian, english)}
    result = r""
    for letter in text:
        if letter in russian:
            result += english_dict[letter]
        elif letter in english:
            result += russian_dict[letter]
        else:
            result += letter
    return result

# .tr       -->        Change text layout
@Client.on_message(filters.command("tr", prefixes=".") & filters.me)
async def translate_message(Client, message):
    try:
        msg = str(message.text).replace(".tr ", "").strip()
        msg_result = await translator(msg)
        await message.edit(msg_result)
    except FloodWait as e:
        time.sleep(e.x)


# .pf        -->        Portfolio
@Client.on_message(filters.command("pf", prefixes="."))
async def my_portfolio(Client, message):
    text = ('<b>Мои проекты на GitHub:</b>\n'
    '<b><a href="https://github.com/darrso/LedMatrixTBot">LedMatrixTBot(aiogram+arduino)</a></b>\n'
    '<i>Бот, предназначенный для рисования на матрице 8x8 с помощью ардуино.</i>\n\n'
    '<b><a href="https://github.com/darrso/parse_channels">Бот-парсер(aiogram+pyrogram)</a></b>\n'
    '<i>Юзер-бот, отслеживающий все телеграм-каналы, на которые он подписан и рассылает новые посты пользователям, которые выбрали тот или иной канал для парсинга.'
    ' Используется aiogram для бота, pyrogram для юзер-бота, sqlalchemy для базы данных.</i>\n\n'
    '<b><a href="https://github.com/darrso/arduino-python-aiogram">3 светодиода бот(aiogram+arduino)</a></b>\n'
    '<i>Простой бот, котролирующий три светодиода, подключенных к ардуино.</i>\n\n'
    '<b><a href="https://github.com/darrso/day_without_bot">... дней без ... бот(aiogram)</a></b>\n'
    '<i>Бот, считающий количество дней, проведенных без чего-то, что пользователь добавил в свой список. Это могут быть сигареты, шоколад и так далее. Используется библиотека PIL для генерации изображений.</i>\n\n'
    '<b><a href="https://github.com/darrso/cute_cal">Калькулятор(pyqt)</a></b>\n'
    '<i>Простой калькулятор, написанный с помощью QtDesigner. Будет грустно, если я его не добавлю в этот список :(</i>')

    adm = await Client.get_me()
    if adm['id'] == message.from_user.id:
        await message.edit(text)
    else:
        await message.reply(text)


# .social       -->        Social
@Client.on_message(filters.command("social", prefixes="."))
async def social(Client, message):
    text = ('<b>Связь со мной:</b>\n'
    '<b>Telegeam</b>: @darrso\n'
    '<b>VK</b>: <a href="vk.com/darrso">@darrso</a>\n'
    '<b>Mail:</b> darrso@yandex.ru')
    adm = await Client.get_me()
    if adm['id'] == message.from_user.id:
        await message.edit(text)
    else:
        await message.reply(text)


# .commands       -->        List of commands
@Client.on_message(filters.command("commands", prefixes="."))
async def check_comands(Client, message):
    text = ('<b>Команды, доступные в данный момент:</b>\n'
    '<b>.tr</b> - перевод текста на другую раскладку\n'
    '<b>.pf</b> - мои проекты на gh\n'
    '<b>.social</b> - связь\n'
    '<b>.commands</b> - команды\n\n'
    '<i>Последнее обновление - 26.03.2022</i>')

    adm = await Client.get_me()
    if adm['id'] == message.from_user.id:
        await message.edit(text)
    else:
        await message.reply(text)

Client.run()