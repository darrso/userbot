import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from googletrans import Translator

# .toen  /  .toru        -->        Google Translate To En From Rus    or    To Rus From En
@Client.on_message(filters.command(["toen", "toru"], prefixes=".") & (filters.private | filters.me) & filters.text)
async def translate_to_en_from_rus(Client, message):
    translator = Translator()
    if message.text[0:5] == ".toen":
        sour, to = "ru", "en"
    else:
        sour, to = "en", "ru"
    text = translator.translate(message.text[6:], src=sour, dest=to).text 
    try:
        adm = await Client.get_me()
        if adm['id'] == message.from_user.id:
            await message.edit(text)
        else:
            await message.reply(text)
    except FloodWait as e:
        time.sleep(e.x)