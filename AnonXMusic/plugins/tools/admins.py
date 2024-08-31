import asyncio
from datetime import datetime, timedelta, timezone
from pyrogram import filters, Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions,
    ChatPrivileges,
    Message
)
from pyrogram.enums import ChatMembersFilter, ChatType
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
from pyrogram.errors import UserNotParticipant
from AnonXMusic import app

# Check if bot has admin rights
async def is_administrator(user_id: int, message, client):
    admin = False
    async for m in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if m.user.id == user_id:
            admin = True
            break
    return admin

@app.on_message(filters.command(["ban"]))
async def banuser(client: Client, message: Message):
    try:
        if not await is_administrator(message.from_user.id, message, client):
            msg = await message.reply_text("You can't do that")
            await asyncio.sleep(5)
            await msg.delete()
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_mention = message.reply_to_message.from_user.mention
        elif len(message.command) > 1:
            user_id = message.text.split(None, 1)[1]
            user_mention = f"[{user_id}](tg://user?id={user_id})"
        else:
            msg = await message.reply_text("Please specify a user to ban.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        await client.ban_chat_member(message.chat.id, user_id)
        msg = await message.reply_text(f"🚫 Banned {user_mention}.")
        await asyncio.sleep(5)
        await msg.delete()

    except Exception as e:
        msg = await message.reply_text(f"Failed to ban {user_mention} due to {e}.")
        await asyncio.sleep(5)
        await msg.delete()