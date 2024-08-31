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

async def is_administrator(user_id: int, message, client):
    async for m in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if m.user.id == user_id:
            return True
    return False

@app.on_message(filters.command(["ban"], prefixes=["/"]) & (filters.group | filters.channel))
async def banuser(client, message):
    try:
        # Check if the message sender is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        # Check if the bot itself is an administrator
        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Determine user to ban
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_mention = message.reply_to_message.from_user.mention
        elif len(message.command) > 1:
            user_id = int(message.text.split(None, 1)[1])
            user_mention = f"[User ID {user_id}](tg://user?id={user_id})"  # User mention link
        else:
            await message.reply_text("Please specify a user to ban.")
            return

        # Perform ban
        await client.ban_chat_member(message.chat.id, user_id)

        # Send a new message to notify about the ban
        await message.reply_text(f"🚫 Banned user with ID {user_id}.")

    except Exception as e:
        # Handle errors
        await message.reply_text(f"Failed to ban user with ID {user_id} due to {e}.")