import os, asyncio, logging, random

import config

from pyrogram import Client, filters, idle
from pyrogram.types import ChatJoinRequest, Message, InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, ChatAdminRequired

from database import add_user, add_group, all_users, all_groups, users, remove_user


app = Client("Approve Bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

welcome=[
    "https://telegra.ph/file/d340ee8523e4d4d850915.mp4",
    "https://telegra.ph/file/51d04427815840250d03a.mp4",
    "https://telegra.ph/file/f41fddb95dceca7b09cbc.mp4",
    "https://telegra.ph/file/a66716c98fa50b2edd63d.mp4",
    "https://telegra.ph/file/17a8ab5b8eeb0b898d575.mp4",
    "https://telegra.ph/file/ced57d72071f4366cd326.mp4"
]



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

# Private Start
@app.on_message(filters.command("start") & filters.private)
async def start(app: Client, msg: Message):
    try:
        await app.get_chat_member(chat_id=config.CHANNEL, user_id=msg.from_user.id)
        add_user(msg.from_user.id)
        await msg.reply_text(text=f"Hey {msg.from_user.mention},\nThis Is {app.me.mention}\n\n> A Powerful Telegram Bot Which Can Accept The User Join Requests Automatically.\n> Just Add {app.me.mention} In Groups And Channels And Make Admin With Proper Rights",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Add {app.name}", url=f"https://t.me/{app.me.username}?startgroup=true")]]))
    except UserNotParticipant:
        await msg.reply_text(text=f"In Order To Use {app.me.mention}, You Must Subscribe To {(await app.get_chat(config.CHANNEL)).title}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join", url=f"https://t.me/{config.CHANNEL}")]]))
    except ChatAdminRequired:
        await app.send_msg(text=f"I'm not admin in fsub chat, Ending fsub...", chat_id=config.OWNER_ID)

# Group Start
@app.on_message(filters.command("start") & filters.group)
async def gc(app: Client, msg: Message):
    add_group(msg.chat.id)
    await msg.reply_text(text=f"{msg.from_user.mention} Start Me In Private For More Info..", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start Me In Private", url=f"https://t.me/{app.me.username}?start=start")]]))

# Stats 
@app.on_message(filters.command("stats"), filters.user(config.OWNER_ID))
async def stat(app: Client, msg: Message):
    user = all_users()
    chat = all_groups()
    await message.reply_text(text=f"Statistics Of {app.me.mention}/n> Users: {user}/n> Chats: {chat}")

#broadcast
@app.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def fcast(app: Client, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "broadcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "broadcast":
                await m.reply_to_message.forward(int(userid))
            except InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")
    

print(f"Starting {app.name}")
app.run()
                           




  


