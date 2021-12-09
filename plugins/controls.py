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

import asyncio
from config import Config
from helpers.log import LOGGER
from pyrogram.types import Message
from pyrogram import Client, filters
from helpers.utils import delete, get_playlist_str, is_admin, mute, restart_playout, skip, pause, resume, unmute, volume, get_buttons, is_admin, seek_file, get_player_string

admin_filter=filters.create(is_admin)


@Client.on_message(filters.command(["playlist", f"playlist@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def c_playlist(client, message):
    pl = await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_text(
            pl,
            disable_web_page_preview=True,
        )
    else:
        if Config.msg.get('playlist') is not None:
            try:
                await Config.msg['playlist'].delete()
            except:
                pass
        Config.msg['playlist'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
        )
        await delete(message)


@Client.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def skip_track(_, m: Message):
    if not Config.playlist:
        k=await m.reply_text("⛔️ **𝙴𝚖𝚙𝚝𝚢 𝙿𝚕𝚊𝚢𝚕𝚒𝚜𝚝 !**")
        await delete(k)
        return
    if len(m.command) == 1:
        await skip()
        await delete(m)
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            for i in items:
                if 2 <= i <= (len(Config.playlist) - 1):
                    Config.playlist.pop(i)
                    k=await m.reply_text(f"⏭ **𝚂𝚞𝚌𝚌𝚎𝚜𝚏𝚞𝚕𝚕𝚢 𝚂𝚔𝚒𝚙𝚙𝚎𝚍 !** \n{i}. **{Config.playlist[i][1]}**")
                    await delete(k)
                else:
                    k=await m.reply_text(f"⛔️ **𝙲𝚊𝚗'𝚝 𝚂𝚔𝚒𝚙 𝙵𝚒𝚛𝚜𝚝 𝚃𝚠𝚘 𝚅𝚒𝚍𝚎𝚘 - {i} !**")
                    await delete(k)
        except (ValueError, TypeError):
            k=await m.reply_text("⛔️ **𝙸𝚗𝚟𝚊𝚕𝚒𝚍 𝙸𝚗𝚙𝚞𝚝 !**")
            await delete(k)
    pl=await get_playlist_str()
    if m.chat.type == "private":
        await m.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        await m.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())


@Client.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def pause_playing(_, m: Message):
    if Config.PAUSE:
        k=await m.reply_text("⏸ **𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝙿𝚊𝚞𝚜𝚎𝚍 !**")
        await delete(k)
        return
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    await pause()
    k=await m.reply_text("⏸ **𝙿𝚊𝚞𝚜𝚎𝚍 𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 !**")
    await delete(k)
    

@Client.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def resume_playing(_, m: Message):
    if not Config.PAUSE:
        k=await m.reply_text("▶️ **𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝙿𝚕𝚊𝚢𝚒𝚗𝚐 !**")
        await delete(k)
        return
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    await resume()
    k=await m.reply_text("▶️ **𝚁𝚎𝚜𝚞𝚖𝚎𝚍 𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 !**")
    await delete(k)


@Client.on_message(filters.command(["volume", f"volume@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def set_vol(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    if len(m.command) < 2:
        k=await m.reply_text("🤖 **𝙿𝚕𝚎𝚊𝚜𝚎 𝙿𝚊𝚜𝚜 𝚅𝚘𝚕𝚞𝚖𝚎 (𝟶-𝟸𝟶𝟶) !**")
        await delete(k)
        return
    await volume(int(m.command[1]))
    k=await m.reply_text(f"🔉 **𝚅𝚘𝚕𝚞𝚖𝚎 𝚂𝚎𝚝 𝚃𝚘 {m.command[1]} !**")
    await delete(k)
    

@Client.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def replay_playout(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    await restart_playout()
    k=await m.reply_text("🔂 **𝚁𝚎𝚙𝚕𝚊𝚢𝚒𝚗𝚐 𝚂𝚝𝚛𝚎𝚊𝚖 !**")
    await delete(k)


@Client.on_message(filters.command(["mute", f"mute@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def set_mute(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    if Config.MUTED:
        k=await m.reply_text("🔇 **𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝙼𝚞𝚝𝚎𝚍 !**")
        await delete(k)
        return
    k=await mute()
    if k:
        s=await m.reply_text(f"🔇 **𝚂𝚞𝚌𝚌𝚎𝚜𝚏𝚞𝚕𝚕𝚢 𝙼𝚞𝚝𝚎𝚍 !**")
        await delete(s)
    else:
        s=await m.reply_text("🔇 **𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝙼𝚞𝚝𝚎𝚍 !**")
        await delete(s)

@Client.on_message(filters.command(["unmute", f"unmute@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def set_unmute(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    if not Config.MUTED:
        k=await m.reply_text("🔊 **𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝚄𝚗𝚖𝚞𝚝𝚎𝚍 !**")
        await delete(k)
        return
    k=await unmute()
    if k:
        s=await m.reply_text(f"🔊 **𝚂𝚞𝚌𝚌𝚎𝚜𝚏𝚞𝚕𝚕𝚢 𝚄𝚗𝚖𝚞𝚝𝚎𝚍 !**")
        await delete(s)
    else:
        s=await m.reply_text("🔊 **𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝚄𝚗𝚖𝚞𝚝𝚎𝚍 !**")
        await delete(s)


@Client.on_message(filters.command(["current", f"current@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def show_current(client, m: Message):
    data=Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        title="▶️ <b>𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 [𝙻𝚒𝚟𝚎 𝚂𝚝𝚛𝚎𝚊𝚖](https://t.me/STMbOTsUPPORTgROUP) !</b>"
    else:
        if Config.playlist:
            title=f"▶️ <b>{Config.playlist[0][1]}</b>"
        elif Config.STREAM_LINK:
            title=f"▶️ <b>𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 [𝚂𝚝𝚛𝚎𝚊𝚖 𝙻𝚒𝚗𝚔]({data['file']}) !</b>"
        else:
            title=f"▶️ <b>𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 [𝚂𝚝𝚊𝚛𝚝𝚞𝚙 𝚂𝚝𝚛𝚎𝚊𝚖]({Config.STREAM_URL}) !</b>"
    if m.chat.type == "private":
        await m.reply_photo(
            photo=Config.THUMB_LINK,
            caption=title,
            reply_markup=await get_buttons()
        )
    else:
        if Config.msg.get('current') is not None:
            try:
                await Config.msg['current'].delete()
            except:
                pass
        Config.msg['current'] = await m.reply_photo(
            photo=Config.THUMB_LINK,
            caption=title,
            reply_markup=await get_buttons()
        )
        await delete(m)


@Client.on_message(filters.command(["seek", f"seek@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def seek_playout(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **𝙳𝚒𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗𝚎𝚍 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝 !**")
        await delete(k)
        return
    if not (Config.playlist or Config.STREAM_LINK):
        k=await m.reply_text("⚠️ **𝚂𝚝𝚊𝚛𝚝𝚞𝚙 𝚂𝚝𝚛𝚎𝚊𝚖 𝙲𝚊𝚗'𝚝 𝙱𝚎 𝚂𝚎𝚎𝚔𝚎𝚍 !**")
        await delete(k)
        return
    data=Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        k=await m.reply_text("⚠️ **𝚃𝚑𝚒𝚜 𝚂𝚝𝚛𝚎𝚊𝚖 𝙲𝚊𝚗'𝚝 𝙱𝚎 𝚂𝚎𝚎𝚔𝚎𝚍 !**")
        await delete(k)
        return
    if ' ' in m.text:
        i, time = m.text.split(" ")
        try:
            time=int(time)
        except:
            k=await m.reply_text("⛔️ **𝙸𝚗𝚟𝚊𝚕𝚒𝚍 𝚃𝚒𝚖𝚎 𝚂𝚙𝚎𝚌𝚒𝚏𝚒𝚎𝚍 !**")
            await delete(k)
            return
        k, string=await seek_file(time)
        if k == False:
            s=await m.reply_text(f"**{string}**")
            await delete(s)
            return
        if not data.get('dur', 0) or \
            data.get('dur') == 0:
            title="▶️ <b>𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 [𝙻𝚒𝚟𝚎 𝚂𝚝𝚛𝚎𝚊𝚖](https://t.me/STMbOTsUPPORTgROUP) !</b>"
        else:
            if Config.playlist:
                title=f"▶️ <b>{Config.playlist[0][1]}</b>"
            elif Config.STREAM_LINK:
                title=f"▶️ <b>𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 [𝚂𝚝𝚛𝚎𝚊𝚖 𝙻𝚒𝚗𝚔]({data['file']}) !</b>"
            else:
                title=f"▶️ <b>𝚂𝚝𝚛𝚎𝚊𝚖𝚒𝚗𝚐 [𝚂𝚝𝚊𝚛𝚝𝚞𝚙 𝚂𝚝𝚛𝚎𝚊𝚖]({Config.STREAM_URL}) !</b>"
        s=await m.reply_text(f"{title}", reply_markup=await get_buttons(), disable_web_page_preview=True)
        await delete(s)
    else:
        s=await m.reply_text("❗ **𝚈𝚘𝚞 𝚂𝚑𝚘𝚞𝚕𝚍 𝚂𝚙𝚎𝚌𝚒𝚏𝚢 𝚃𝚑𝚎 𝚃𝚒𝚖𝚎 𝙸𝚗 𝚂𝚎𝚌𝚘𝚗𝚍 𝚃𝚘 𝚂𝚎𝚎𝚔!** \n\n𝙵𝚘𝚛 𝙴𝚡𝚊𝚖𝚙𝚕𝚎: \n• `/𝚜𝚎𝚎𝚔 𝟷𝟶` 𝚝𝚘 𝚏𝚘𝚠𝚊𝚛𝚍 𝟷𝟶 𝚜𝚎𝚌. \n• `/seek -𝟷𝟶` 𝚝𝚘 𝚛𝚎𝚠𝚒𝚗𝚍 𝟷𝟶 𝚜𝚎𝚌.")
        await delete(s)
