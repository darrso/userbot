import asyncio
from pyrogram import Client, idle


async def main():
    await Client("darrso").start()
    print("Bot started!")
    await idle()
    print("Bot closed!")

if __name__ == "__main__":
    asyncio.run(main())