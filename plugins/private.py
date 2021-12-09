"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import sys
import asyncio
from config import Config
from helpers.log import LOGGER
from pyrogram import Client, filters
from helpers.utils import delete, update, is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument


HOME_TEXT = "👋🏻 **Hᴇʟʟᴏ [{}](tg://user?id={})**, \n\nI'ᴍ **Vɪᴅᴇᴏ Pʟᴀʏᴇʀ Bᴏᴛ**. \nI Cᴀɴ Sᴛʀᴇᴀᴍ Lɪᴠᴇs, YᴏᴜTᴜʙᴇ Vɪᴅᴇᴏs & Tᴇʟᴇɢʀᴀᴍ Vɪᴅᴇᴏ Fɪʟᴇs Oɴ Vɪᴅᴇᴏ Cʜᴀᴛ Oғ Tᴇʟᴇɢʀᴀᴍ Cʜᴀɴɴᴇʟs & Gʀᴏᴜᴘs 😉! \n\n**Mᴀᴅᴇ Wɪᴛʜ ❤️ Bʏ [ᔆᵀᴹ](https://t.me/storytym) !** 👑"
HELP_TEXT = """
💡 --**Sᴇᴛᴛɪɴɢ Uᴘ**--:

\u2022 Aᴅᴅ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀᴅᴍɪɴ ʀɪɢʜᴛs.
\u2022 Sᴛᴀʀᴛ ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ & ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ɪғ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴛᴏ ᴠᴄ.
\u2022 Usᴇ /play [ᴠɪᴅᴇᴏ ɴᴀᴍᴇ] ᴏʀ ᴜsᴇ /play ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴏʀ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ.

💡 --**Cᴏᴍᴍᴏɴ Cᴏᴍᴍᴀɴᴅs**--:

\u2022 `/start` - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
\u2022 `/help` - sʜᴏᴡs ᴛʜᴇ ʜᴇʟᴘ
\u2022 `/current` - sʜᴏᴡ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ
\u2022 `/playlist` - sʜᴏᴡs ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ

💡 --**Aᴅᴍɪɴs Cᴏᴍᴍᴀɴᴅs**--:

\u2022 `/seek` - sᴇᴇᴋ ᴛʜᴇ ᴠɪᴅᴇᴏ
\u2022 `/skip` - sᴋɪᴘ ᴄᴜʀʀᴇɴᴛ ᴠɪᴅᴇᴏ
\u2022 `/stream` - sᴛᴀʀᴛ ʟɪᴠᴇ sᴛʀᴇᴀᴍ
\u2022 `/pause` - ᴘᴀᴜsᴇ ᴘʟᴀʏɪɴɢ ᴠɪᴅᴇᴏ
\u2022 `/resume` - ʀᴇsᴜᴍᴇ ᴘʟᴀʏɪɴɢ ᴠɪᴅᴇᴏ
\u2022 `/mute` - ᴍᴜᴛᴇ ᴛʜᴇ ᴠᴄ ᴜsᴇʀʙᴏᴛ
\u2022 `/unmute` - ᴜɴᴍᴜᴛᴇ ᴛʜᴇ ᴠᴄ ᴜsᴇʀʙᴏᴛ
\u2022 `/leave` - ʟᴇᴀᴠᴇ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ
\u2022 `/shuffle` - sʜᴜғғʟᴇ ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ
\u2022 `/volume` - ᴄʜᴀɴɢᴇ ᴠᴄ ᴠᴏʟᴜᴍᴇ (0-200)
\u2022 `/replay` - ᴘʟᴀʏ ғʀᴏᴍ ᴛʜᴇ ʙᴇɢɪɴɴɪɴɢ
\u2022 `/clrlist` - ᴄʟᴇᴀʀ ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ ᴏ̨ᴜᴇᴜᴇ
\u2022 `/restart` - ᴜᴘᴅᴀᴛᴇ & ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
\u2022 `/setvar` - sᴇᴛ/ᴄʜᴀɴɢᴇ ʜᴇʀᴏᴋᴜ ᴄᴏɴғɪɢs
\u2022 `/getlogs` - ɢᴇᴛ ᴛʜᴇ ғғᴍᴘᴇɢ & ʙᴏᴛ ʟᴏɢs

© **Pᴏᴡᴇʀᴇᴅ Bʏ** : 
**[ᔆᵀᴹ 👑](https://t.me/storytym)** 
"""

admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(["start", f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("𝚂𝙴𝙰𝚁𝙲𝙷 𝚅𝙸𝙳𝙴𝙾𝚂", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("𝙲𝙷𝙰𝙽𝙽𝙴𝙻", url="https://t.me/storytimeoGG"),
                InlineKeyboardButton("𝙰𝙽𝚈 𝙷𝙴𝙻𝙿", url="https://t.me/STMbOTsUPPORTgROUP"),
            ],
            [
                InlineKeyboardButton("𝙱𝙾𝚃 𝙴𝙳𝚃𝙾𝚁", url="https://t.me/VAMPIRE_KING_NO_1"),
                InlineKeyboardButton("𝙼𝙾𝚅𝙸𝙴 𝙶𝚁𝙾𝚄𝙿", url="https://t.me/storytym"),
            ],
            [
                InlineKeyboardButton("𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo=Config.THUMB_LINK, caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await delete(m)


@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    buttons = [
            [
                InlineKeyboardButton("𝚂𝙴𝙰𝚁𝙲𝙷 𝚅𝙸𝙳𝙴𝙾𝚂", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("𝙲𝙷𝙰𝙽𝙽𝙴𝙻", url="https://t.me/storytimeoGG"),
                InlineKeyboardButton("𝙰𝙽𝚈 𝙷𝙴𝙻𝙿", url="https://t.me/STMbOTsUPPORTgROUP"),
            ],
            [
                InlineKeyboardButton("𝙱𝙾𝚃 𝙴𝙳𝚃𝙾𝚁", url="t.me/VAMPIRE_KING_NO_1"),
                InlineKeyboardButton("𝙼𝙾𝚅𝙸𝙴 𝙶𝚁𝙾𝚄𝙿", url="https://t.me/storytym"),
            ],
            [
                InlineKeyboardButton("𝙱𝙰𝙲𝙺 𝙷𝙾𝙼𝙴", callback_data="home"),
                InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴 𝙼𝙴𝙽𝚄", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if Config.msg.get('help') is not None:
        try:
            await Config.msg['help'].delete()
        except:
            pass
    Config.msg['help'] = await message.reply_photo(photo=Config.THUMB_LINK, caption=HELP_TEXT, reply_markup=reply_markup)
    await delete(message)


@Client.on_message(filters.command(["restart", "update", f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    k=await message.reply_text("🔄 **Checking ...**")
    await asyncio.sleep(3)
    if Config.HEROKU_APP:
        await k.edit("🔄 **Heroku Detected, \nRestarting App To Update!**")
    else:
        await k.edit("🔄 **Restarting, Please Wait...**")
    await update()
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin @storytimeoG For Update!**")
        await k.reply_to_message.delete()
    except:
        pass


@Client.on_message(filters.command(["getlogs", f"getlogs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="Video Player Logs"))
    if logs:
        try:
            await message.reply_media_group(logs)
            await delete(message)
        except:
            m=await message.reply_text("❌ **An Error Occoured !**")
            await delete(m)
            pass
        logs.clear()
    else:
        m=await message.reply_text("❌ **No Log Files Found !**")
        await delete(m)


@Client.on_message(filters.command(["setvar", f"setvar@{Config.BOT_USERNAME}"]) & admin_filter)
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        k=await message.reply_text(
            text="❗ **No Heroku App Found !** \n__Please Note That, This Command Needs The Following Heroku Vars To Be Set :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @AsmSupport !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        await delete(k)
        return     
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            k=await message.reply_text("❗ **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001313215676`")
            await delete(k)
            return
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"❗ **No Value Specified, So Deleting `{var}` Variable !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"🗑 **Sucessfully Deleted `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"🤷‍♂️ **Variable Named `{var}` Not Found, Nothing Was Changed !**")
            return
        if var in config:
            m=await message.reply_text(f"⚠️ **Variable Already Found, So Edited Value To `{value}` !**")
        else:
            m=await message.reply_text(f"⚠️ **Variable Not Found, So Setting As New Var !**")
        await asyncio.sleep(2)
        await m.edit(f"✅ **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
        await delete(m)
    else:
        k=await message.reply_text("❗ **You Haven't Provided Any Variable, You Should Follow The Correct Format !** \n\nFor Example: \n• `/setvar CHAT_ID=-1001313215676` to change or set CHAT_ID var. \n• `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.")
        await delete(k)
