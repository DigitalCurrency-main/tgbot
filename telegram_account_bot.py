from telethon.sync import TelegramClient, events

api_id = 28169155
api_hash = "d59f7e9f5a929e4a9b2da02daa1a1a00"

with TelegramClient('session_name', api_id, api_hash) as client:

   @client.on(events.NewMessage())
   async def handler(event):
      await event.reply('Hey!')

   client.run_until_disconnected()