import os, asyncio, logging, random

import config

from pyrogram import Client, filters, idle
from pyrogram.types import ChatJoinRequest, Message, InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram.errors import FloodWait, MessageNotModified, UserIsBlocked, PeerIdInvalid, 

from database import add_user, add_group, all_users, all_groups, users, remove_user


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

welcome=[
    "https://telegra.ph/file/d340ee8523e4d4d850915.mp4",
    "https://telegra.ph/file/51d04427815840250d03a.mp4",
    "https://telegra.ph/file/f41fddb95dceca7b09cbc.mp4",
    "https://telegra.ph/file/a66716c98fa50b2edd63d.mp4",
    "https://telegra.ph/file/17a8ab5b8eeb0b898d575.mp4",
    "https://telegra.ph/file/ced57d72071f4366cd326.mp4"
]

async def run_bot_():
    await app.start()
    await idle()

async def run_ass_():
    await ass.start()

# Approve request
@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approval(app: Client, m: ChatJoinRequest):
    user = m.from_user
    chat = m.chat
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(chat.id, user.id)
        gif = random.choice(welcome)
        await app.send_animation(animation=gif, caption=f"Hey There {user.first_name}\nWelcome To {chat.title}", chat_id=user.id)
        add_user(user.id)
    except (UserIsBlocked, PeerIdInvalid):
        pass
    except Exception as err:
        print(str(err))    

# Start 
@app.on_message(filters.command("start"))
async def start(app: Client, msg: Message):
  await msg.reply_text(text=f"Hey {msg.from_user.mention},\nThis Is {app.me.mention}\n\n> A Powerful Telegram Bot Which Can Accept The User Join Requests Automatically.\n> Just Add Ne In The Chat And Make Me Admin With Proper Rights",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Add {app.name}", url=f"https://t.me/{app.me.username}?startgroup=true")]])
                           )


print("Starting")
if __name__ == "__main__":
    app.loop.run_until_complete(run_bot_())
                           




  


