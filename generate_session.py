from telethon import TelegramClient

api_id = 28169155
api_hash = "d59f7e9f5a929e4a9b2da02daa1a1a00"

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()
    print("Logged in!")

client.loop.run_until_complete(main())