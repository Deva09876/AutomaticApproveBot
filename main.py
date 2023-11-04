import os, asyncio, logging

import config

from pyrogram import Client, filters, idle
from pyrogram.types import ChatJoinRequest, Message, InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram.errors import FloodWait, MessageNotModified, UserIsBlocked, PeerIdInvalid

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

app = Client("Approve Bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)
ass = Client("Approve Ass", api_id=config.API_ID, api_hash=config.API_HASH, session_string=config.SESSION)

async def run_bot_():
    await app.start()
    await idle()

@app.on_chat_join_request(filters.group & filters.channel)
async def approval(app: Client, m: ChatJoinRequest):
  user = m.from_user
  chat = m.chat
  if not m.from_user:
        return
    try
        await app.approve_chat_join_request(chat.id, user.id)
    except FloodWait as e:
        logging.info(f"Sleeping for {e.x + 3} seconds due to floodwaits!")
        await asyncio.sleep(e.x + 3)
        await app.approve_chat_join_request(chat.id, user.id)
    try:
    await app.send_message(user.id, f"Hey {user.mention}👋, Your Request To Join {chat.title} Has Been Accepted!")
  except (UserIsBlocked, PeerIdInvalid):
        pass

@app.on_message(filters.command("start"))
async def start(app: Client, msg: Message):
  await message.reply_photo(photo=config.START_IMG, caption=f"Hey {msg.from_user.mention},\nThis Is {app.mention}\n\n> A Powerful Telegram Bot Which Can Accept The User Join Requests Automatically.\n> Just Add Ne In The Chat And Make Me Admin With Proper Rights",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Add {app.name}", url=f"https://t.me/{app.username}?startgroup=true")]])
                           )


print("Starting")
if __name__ == "__main__":
    app.loop.run_until_complete(run_bot_())
                           




  

