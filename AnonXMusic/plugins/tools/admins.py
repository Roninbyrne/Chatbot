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
    async for m in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if m.user.id == user_id:
            return True
    return False

@app.on_message(filters.command(["ban"]))
async def banuser(client: Client, message: Message):
    admin_mention = message.from_user.mention  # Mention of the user issuing the command
    user_mention = None
    user_id = None  # Initialize user_id here
    
    try:
        # Check if the user issuing the command is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            msg = await message.reply_text("🚫 You don't have the permissions to use this command.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        # Determine the user to ban
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_mention = message.reply_to_message.from_user.mention
        elif len(message.command) > 1:
            user_id = message.text.split(None, 1)[1]
            user_mention = f"[{user_id}](tg://user?id={user_id})"
        else:
            msg = await message.reply_text("⚠️ Please specify a user to ban. Reply to their message or include their user ID.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        # Ban the user
        await client.ban_chat_member(message.chat.id, user_id)
        ban_message = f"🚫 **User {user_mention}** has been banned by {admin_mention}."

    except Exception as e:
        # Provide a default mention if user_mention wasn't set before the exception
        if user_mention is None:
            user_mention = f"[{user_id}](tg://user?id={user_id})" if user_id else "the user"
        ban_message = f"❌ Failed to ban {user_mention}. Error: {e}"

    # Send the message and delete it after 5 seconds
    msg = await message.reply_text(ban_message, parse_mode='MarkdownV2')
    await asyncio.sleep(5)
    await msg.delete()