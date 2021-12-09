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
import re
import asyncio
from config import Config
from datetime import datetime
from helpers.log import LOGGER
from youtube_dl import YoutubeDL
from pyrogram.types import Message
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.utils import delete, download, get_admins, is_admin, get_buttons, get_link, leave_call, play, get_playlist_str, send_playlist, shuffle_playlist, start_stream, stream_from_link

admin_filter=filters.create(is_admin)


@Client.on_message(filters.command(["play", f"play@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def add_to_playlist(_, message: Message):
    if Config.ADMIN_ONLY == "True":
        admins = await get_admins(Config.CHAT_ID)
        if message.from_user.id not in admins:
            k=await message.reply_sticker("CAACAgQAAxkBAAEDcQphsX2yLebHke-DAkWg0CT-XgUJ5gACwwcAArVKOFN1CWCsUCW1GSME")
            await delete(k)
            return
    type=""
    yturl=""
    ysearch=""
    if message.reply_to_message and message.reply_to_message.video:
        msg = await message.reply_text("⚡️")
        type='video'
        m_video = message.reply_to_message.video       
    elif message.reply_to_message and message.reply_to_message.document:
        msg = await message.reply_text("⚡️")
        m_video = message.reply_to_message.document
        type='video'
        if not "video" in m_video.mime_type:
            k=await msg.edit("⛔️ **𝙸𝚗𝚟𝚊𝚕𝚒𝚍 𝚅𝚒𝚍𝚎𝚘 𝙵𝚒𝚕𝚎 𝙿𝚛𝚘𝚟𝚒𝚍𝚎𝚍!**")
            await delete(k)
            return
    else:
        if message.reply_to_message:
            link=message.reply_to_message.text
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex,link)
            if match:
                type="youtube"
                yturl=link
        elif " " in message.text:
            text = message.text.split(" ", 1)
            query = text[1]
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex,query)
            if match:
                type="youtube"
                yturl=query
            else:
                type="query"
                ysearch=query
        else:
            k=await message.reply_text("❗ __**𝚂𝚎𝚗𝚍 𝙼𝚎 𝙰𝚗 𝚈𝚘𝚞𝚃𝚞𝚋𝚎 𝚅𝚒𝚍𝚎𝚘 𝙽𝚊𝚖𝚎 / 𝚈𝚘𝚞𝚃𝚞𝚋𝚎 𝚅𝚒𝚍𝚎𝚘 𝙻𝚒𝚗𝚔 / 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚒𝚍𝚎𝚘 𝚃𝚘 𝙿𝚕𝚊𝚢 𝙸𝚗 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**__")
            await delete(k)
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if type=="video":
        now = datetime.now()
        lel = now.strftime("%d-%m-%Y-%H:%M:%S")
        data={1:m_video.file_name, 2:m_video.file_id, 3:"telegram", 4:user, 5:f"{lel}_{m_video.file_size}"}
        Config.playlist.append(data)
        await msg.edit("➕ **𝙼𝚎𝚍𝚒𝚊 𝙰𝚍𝚍𝚎𝚍 𝚃𝚘 𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 !**")
    if type=="youtube" or type=="query":
        if type=="youtube":
            msg = await message.reply_text("🔎")
            url=yturl
        elif type=="query":
            try:
                msg = await message.reply_text("🔎")
                ytquery=ysearch
                results = YoutubeSearch(ytquery, max_results=1).to_dict()
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
            except Exception as e:
                k=await msg.edit(
                    "**𝙻𝚒𝚝𝚎𝚛𝚊𝚛𝚢 𝙵𝚘𝚞𝚗𝚍 𝙽𝚘𝚝𝚒𝚗𝚐 !\n𝚃𝚛𝚢 𝚂𝚎𝚊𝚛𝚌𝚑𝚒𝚗𝚐 𝙾𝚗 𝙸𝚗𝚕𝚒𝚗𝚎 𝙼𝚘𝚍𝚎 😉!**"
                )
                LOGGER.error(str(e))
                await delete(k)
                return
        else:
            return
        ydl_opts = {
            "geo-bypass": True,
            "nocheckcertificate": True
        }
        ydl = YoutubeDL(ydl_opts)
        try:
            info = ydl.extract_info(url, False)
        except Exception as e:
            LOGGER.error(e)
            k=await msg.edit(
                f"❌ **𝚈𝚘𝚞𝚃𝚞𝚋𝚎 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙴𝚛𝚛𝚘𝚛 !** \n\n{e}"
                )
            LOGGER.error(str(e))
            await delete(k)
            return
        title = info["title"]
        now = datetime.now()
        lel = now.strftime("%d-%m-%Y-%H:%M:%S")
        data={1:title, 2:url, 3:"youtube", 4:user, 5:f"{lel}_{message.from_user.id}"}
        Config.playlist.append(data)
        await msg.edit(f"➕ **[{title}]({url}) 𝙰𝚍𝚍𝚎𝚍 𝚃𝚘 𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 !**", disable_web_page_preview=True)
    if len(Config.playlist) == 1:
        m_status = await msg.edit("⚡️")
        await download(Config.playlist[0], m_status)
        await m_status.delete()
        await play()
    else:
        await send_playlist()
        await delete(msg)
    pl=await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and message.chat.type == "supergroup":
        await message.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())
    await delete(message)
    for track in Config.playlist[:2]:
        await download(track)


@Client.on_message(filters.command(["leave", f"leave@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def leave_voice_chat(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    await leave_call()
    k=await m.reply_text("✅ **𝙻𝚎𝚏𝚝 𝙵𝚛𝚘𝚖 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
    await delete(k)


@Client.on_message(filters.command(["shuffle", f"shuffle@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def shuffle_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
    else:
        if len(Config.playlist) > 2:
            await shuffle_playlist()
            k=await m.reply_text(f"🔄 **𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 𝚂𝚑𝚞𝚏𝚏𝚕𝚎𝚍 !**")
            await delete(k)
        else:
            k=await m.reply_text(f"⛔️ **𝙲𝚊𝚗'𝚝 𝚂𝚑𝚞𝚏𝚏𝚕𝚎 𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 𝙵𝚘𝚛 𝙻𝚎𝚜𝚜 𝚃𝚑𝚊𝚗 𝟹 𝚅𝚒𝚍𝚎𝚘 !**")
            await delete(k)


@Client.on_message(filters.command(["clrlist", f"clrlist@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def clear_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    if not Config.playlist:
        k=await m.reply_text("⛔️ **𝙴𝚖𝚙𝚝𝚢 𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 !**")
        await delete(k)
        return
    Config.playlist.clear()   
    k=await m.reply_text(f"✅ **𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 𝙲𝚕𝚎𝚊𝚛𝚎𝚍!**")
    await delete(k)
    await start_stream()


@Client.on_message(filters.command(["stream", f"stream@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def stream(client, m: Message):
    if m.reply_to_message:
        link=m.reply_to_message.text
    elif " " in m.text:
        text = m.text.split(" ", 1)
        link = text[1]
    else:
        k=await m.reply_text("❗ __**𝚂𝚎𝚗𝚍 𝙼𝚎 𝙰𝚗 𝙻𝚒𝚟𝚎 𝚂𝚝𝚛𝚎𝚊𝚖 𝙻𝚒𝚗𝚔 / 𝚈𝚘𝚞𝚃𝚞𝚋𝚎 𝙻𝚒𝚟𝚎 𝚂𝚝𝚛𝚎𝚊𝚖 𝙻𝚒𝚗𝚔 𝚃𝚘 𝚂𝚝𝚊𝚛𝚝 𝙻𝚒𝚟𝚎 𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 !**__")
        await delete(k)
        return
    regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
    match = re.match(regex,link)
    if match:
        stream_link=await get_link(link)
        if not stream_link:
            k=await m.reply_text("⛔️ **𝙸𝚗𝚟𝚊𝚕𝚒𝚍 𝚂𝚝𝚛𝚎𝚊𝚖 𝙻𝚒𝚗𝚔 𝙿𝚛𝚘𝚟𝚒𝚍𝚎𝚍 !**")
            await delete(k)
            return
    else:
        stream_link=link
    k, msg=await stream_from_link(stream_link)
    if k == False:
        s=await m.reply_text(msg)
        await delete(s)
        return
    s=await m.reply_text(f"▶️ **𝚂𝚝𝚊𝚛𝚝𝚎𝚍 [𝙻𝚒𝚟𝚎 𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐]({stream_link}) !**", disable_web_page_preview=True)
    await delete(s)


admincmds=["join", "leave", "pause", "resume", "skip", "restart", "volume", "shuffle", "clrlist", "update", "replay", "getlogs", "stream", "mute", "unmute", "seek", f"mute@{Config.BOT_USERNAME}", f"unmute@{Config.BOT_USERNAME}", f"seek@{Config.BOT_USERNAME}", f"stream@{Config.BOT_USERNAME}", f"getlogs@{Config.BOT_USERNAME}", f"replay@{Config.BOT_USERNAME}", f"join@{Config.BOT_USERNAME}", f"leave@{Config.BOT_USERNAME}", f"pause@{Config.BOT_USERNAME}", f"resume@{Config.BOT_USERNAME}", f"skip@{Config.BOT_USERNAME}", f"restart@{Config.BOT_USERNAME}", f"volume@{Config.BOT_USERNAME}", f"shuffle@{Config.BOT_USERNAME}", f"clrlist@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]

@Client.on_message(filters.command(admincmds) & ~admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def notforu(_, m: Message):
    k=await _.send_cached_media(chat_id=m.chat.id, file_id="CAACAgUAAxkBAAEB1GNhO2oHEh2OqrpucczIprmOIEKZtQACfwMAAjSe9DFG-UktB_TxOh4E", caption="**𝚈𝚘𝚞 𝙰𝚛𝚎 𝙽𝚘𝚝 𝙰𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 !!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚡️ 𝙹𝚘𝚒𝚗 𝙷𝚎𝚛𝚎 ⚡️', url='https://t.me/STMbOTsUPPORTgROUP')]]), reply_to_message_id=m.message_id)
    await delete(k)

allcmd = ["play", "current", "playlist", f"play@{Config.BOT_USERNAME}", f"current@{Config.BOT_USERNAME}", f"playlist@{Config.BOT_USERNAME}"] + admincmds

@Client.on_message(filters.command(allcmd) & filters.group & ~(filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def not_chat(_, m: Message):
    buttons = [
            [
                InlineKeyboardButton("𝙲𝙷𝙰𝙽𝙽𝙴𝙻", url="https://t.me/storytimeoGG"),
                InlineKeyboardButton("𝙰𝙽𝚈 𝙷𝙴𝙻𝙿", url="https://t.me/STMbOTsUPPORTgROUP"),
            ],
            [
                InlineKeyboardButton("𝙼𝙾𝚅𝙸𝙴 𝙶𝚁𝙾𝚄𝙿", url="https://t.me/storytym"),
            ]
         ]
    await m.reply_photo(photo=Config.THUMB_LINK, caption="**Bruh, 𝚈𝚘𝚞 𝙲𝚊𝚗'𝚝 𝚄𝚜𝚎 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙸𝚗 𝚃𝚑𝚒𝚜 𝙶𝚛𝚘𝚞𝚙 🤷‍♂️! 𝙹𝚘𝚒𝚗 𝙾𝚞𝚛 [𝙶𝚛𝚘𝚞𝚙](https://t.me/STMbOTsUPPORTgROUP) 𝙵𝚘𝚛 𝙰𝚗𝚢 𝙷𝚎𝚕𝚙 !**", reply_markup=InlineKeyboardMarkup(buttons))
