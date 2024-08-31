import asyncio
from datetime import datetime, timedelta, timezone

from pyrogram import filters, Client
from pyrogram.types import ChatPrivileges, ChatPermissions, Message
from pyrogram.enums import ChatMembersFilter, ChatType
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, BadRequest
from pyrogram.errors import UserNotParticipant

# Check if bot has admin rights
async def is_administrator(user_id: int, message,client):
    admin = False
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for user in administrators:
        if user.user.id == user_id:
            admin = True
            break
    return admin
async def is_admin(user_id: int, message):

    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    if user_id in administrators:
        return True     
    else:
        return False



@app.on_message(filters.command(["ban"]))
async def banuser(b, message):
    try:
        if not is_admin(message.from_user.id, message):
            msg = await message.edit_text("You can't do that")
            await asyncio.sleep(5)
            await msg.delete()
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_mention = message.reply_to_message.from_user.mention
        elif len(message.command) > 1:
            user_id = message.text.split(None, 1)[1]
            user_mention = user_id
        else:
            msg = await message.edit_text("Please specify a user to ban.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        await b.ban_chat_member(message.chat.id, user_id)
        msg = await message.edit_text(f"🚫 Banned {message.from_user.mention}.")
        await asyncio.sleep(5)
        await msg.delete()

    except Exception as e:
        msg = await message.edit_text(f"Failed to ban {user_mention} due to {e}.")
        await asyncio.sleep(5)
        await msg.delete()