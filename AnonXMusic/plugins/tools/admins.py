import asyncio
from datetime import datetime, timedelta, timezone
from pyrogram import Client, filters
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
from pyrogram.errors import UsernameNotOccupied, UserNotParticipant
from AnonXMusic import app  # Importing the app object from your project

async def is_administrator(user_id: int, message, client):
    async for m in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if m.user.id == user_id:
            return True
    return False

async def is_bot_administrator(message, client):
    bot_user_id = (await client.get_me()).id
    async for m in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if m.user.id == bot_user_id:
            return True
    return False

async def resolve_username_to_id(username: str, client):
    try:
        user = await client.get_users(username)
        return user.id
    except UsernameNotOccupied:
        return None

@app.on_message(filters.command(["ban"], prefixes=["/"]) & (filters.group | filters.channel))
async def banuser(client, message):
    user_id = None  # Initialize user_id
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
        elif len(message.command) > 1:
            arg = message.text.split(None, 1)[1]
            if arg.startswith('@'):
                # Handle username
                username = arg[1:]  # Remove '@'
                user_id = await resolve_username_to_id(username, client)
                if user_id is None:
                    await message.reply_text("Username not found.")
                    return
            else:
                # Handle user ID
                try:
                    user_id = int(arg)
                except ValueError:
                    await message.reply_text("Invalid user ID.")
                    return

        if user_id is None:
            await message.reply_text("Please specify a user to ban.")
            return

        # Perform ban
        await client.ban_chat_member(message.chat.id, user_id)

        # Send a new message to notify about the ban
        await message.reply_text(f"🚫 Banned user with ID {user_id}.")

    except Exception as e:
        # Handle errors
        await message.reply_text(f"Failed to ban user due to {e}.")