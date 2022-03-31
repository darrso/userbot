import time

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

import wikipedia as wiki
from wikipedia.exceptions import DisambiguationError
wiki.set_lang("ru")


# pages - dict {"name of page":"summary"}
# page_names - 3 page names

async def wiki_search(word):
    pages = dict()
    word = (word.strip())
    page_names = wiki.search(word, results=3)

    # Bad request, Returns "Nothing found" and bool false for answer without errors
    if not page_names:
        return "Ничего не найдено!", False
    else:
        try:
            for name in page_names:
                page = wiki.page(name)
                
                # Length limit - 4 sentences
                pages[name] = f'{". ".join(str(page.summary).split(". ")[0:4])}'

                # Adding a link to a new line
                pages[name] += f"\n{page.url}"
            
            # Returns dict and bool
            return pages, True

        # Ambiguity in the request
        except DisambiguationError as e:

            # 5 similar queries
            e = "\n".join(str(e).split('\n')[0:5])
            return f"Неоднозначно! {e}", False


async def get_text(pages):
    result = ""
    for key, value in pages.items():
        summar = value.split("\n")
        # SUMMAR[-1] - URL
        # KEY - NAME
        # SUMMAR[0:-1] - SUMMARY WITHOUT URL
        result += f'<b><i><u><a href={summar[-1]}>{key}</a></u></i></b>\n{" ".join(summar[:-1])}\n\n'
    return result


# .wiki or "что такое ..."       -->        Wiki result
# filters - text(avoid error in lambda function) AND private(message in pm)  AND (("что такое" in message) OR .wiki command )
@Client.on_message(filters.text & (filters.create(lambda _, __, message: "что такое" == message.text.lower()[0:9]) \
    | filters.command("wiki", prefixes=".")) & filters.private)
async def send_wiki_result_on_command(Client, message):
    # IF .wiki command - message.text[0:5] == ".wiki"
    # ELIF "что такое" command - message.text[0:9] == "что такое"
    if (message.text[9:] != "" and message.text[0:9].lower() == "что такое") or (message.text[6:] != "" and message.text[0:5] == ".wiki"):
        search = message.text[6:] if message.text[0:5] == ".wiki" else message.text[9:]
        pages, flag = await wiki_search(search) 
        if flag:    
            text = await get_text(pages)
        else:
            text = pages
        try:
            await message.reply(text)
        except FloodWait as e:
            time.sleep(e.x)