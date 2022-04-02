import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait


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
