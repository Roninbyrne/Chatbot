import asyncio
from datetime import datetime, timedelta, timezone
from pyrogram import Client, filters, types
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
from pyrogram.errors import UsernameNotOccupied, UserNotParticipant, FloodWait
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

@app.on_message(filters.command(["ban"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def banuser(client, message):
    user_id = None  # Initialize user_id
    reason = None  # Initialize reason
    try:
        # Check if the message sender is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        # Check if the bot itself is an administrator
        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Determine user to ban and reason
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            # Split command text based on spaces, but handle the case where reason might include spaces
            args = message.text.split(None, 1)[1]
            if args.startswith('@'):
                # Handle username
                username = args[1:].split()[0]  # Extract username
                user_id = await resolve_username_to_id(username, client)
                if user_id is None:
                    await message.reply_text("Username not found.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])
            else:
                # Handle user ID
                try:
                    user_id = int(args.split()[0])
                except ValueError:
                    await message.reply_text("Invalid user ID.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])

        if user_id is None:
            await message.reply_text("Please specify a user to ban.")
            return

        # Perform ban
        await client.ban_chat_member(message.chat.id, user_id)

        # Get user and admin info
        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name
        reason_text = f" Reason: {reason}" if reason else ""

        # Send a new message to notify about the ban
        await message.reply_text(f"{user_name} has been banned by {admin_name}.{reason_text}")

    except Exception as e:
        # Handle errors
        await message.reply_text(f"Failed to ban user due to {e}.")


@app.on_message(filters.command(["unban"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def unbanuser(client, message):
    user_id = None  # Initialize user_id
    reason = None  # Initialize reason
    try:
        # Check if the message sender is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        # Check if the bot itself is an administrator
        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Determine user to unban and reason
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            # Split command text based on spaces, but handle the case where reason might include spaces
            args = message.text.split(None, 1)[1]
            if args.startswith('@'):
                # Handle username
                username = args[1:].split()[0]  # Extract username
                user_id = await resolve_username_to_id(username, client)
                if user_id is None:
                    await message.reply_text("Username not found.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])
            else:
                # Handle user ID
                try:
                    user_id = int(args.split()[0])
                except ValueError:
                    await message.reply_text("Invalid user ID.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])

        if user_id is None:
            await message.reply_text("Please specify a user to unban.")
            return

        # Perform unban
        await client.unban_chat_member(message.chat.id, user_id)

        # Get user and admin info
        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name
        reason_text = f" Reason: {reason}" if reason else ""

        # Send a new message to notify about the unban
        await message.reply_text(f"{user_name} has been unbanned by {admin_name}.{reason_text}")

    except Exception as e:
        # Handle errors
        await message.reply_text(f"Failed to unban user due to {e}.")


@app.on_message(filters.command(["mute"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def mute_user(client, message):
    user_id = None  # Initialize user_id
    reason = None  # Initialize reason
    try:
        # Check if the message sender is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        # Check if the bot itself is an administrator
        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Determine user to mute and reason
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            # Split command text based on spaces, but handle the case where reason might include spaces
            args = message.text.split(None, 1)[1]
            if args.startswith('@'):
                # Handle username
                username = args[1:].split()[0]  # Extract username
                user_id = await resolve_username_to_id(username, client)
                if user_id is None:
                    await message.reply_text("Username not found.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])
            else:
                # Handle user ID
                try:
                    user_id = int(args.split()[0])
                except ValueError:
                    await message.reply_text("Invalid user ID.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])

        if user_id is None:
            await message.reply_text("Please specify a user to mute.")
            return

        # Perform mute
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )

        # Get user and admin info
        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name
        reason_text = f" Reason: {reason}" if reason else ""

        # Send a new message to notify about the mute
        await message.reply_text(f"{user_name} has been muted by {admin_name}.{reason_text}")

    except Exception as e:
        # Handle errors
        await message.reply_text(f"Failed to mute user due to {e}.")


@app.on_message(filters.command(["unmute"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def unmute_user(client, message):
    user_id = None  # Initialize user_id
    reason = None  # Initialize reason
    try:
        # Check if the message sender is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        # Check if the bot itself is an administrator
        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Determine user to unmute and reason
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            # Split command text based on spaces, but handle the case where reason might include spaces
            args = message.text.split(None, 1)[1]
            if args.startswith('@'):
                # Handle username
                username = args[1:].split()[0]  # Extract username
                user_id = await resolve_username_to_id(username, client)
                if user_id is None:
                    await message.reply_text("Username not found.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])
            else:
                # Handle user ID
                try:
                    user_id = int(args.split()[0])
                except ValueError:
                    await message.reply_text("Invalid user ID.")
                    return
                # Extract reason if available
                reason = ' '.join(args.split()[1:])

        if user_id is None:
            await message.reply_text("Please specify a user to unmute.")
            return

        # Perform unmute
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True
            )
        )

        # Get user and admin info
        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name
        reason_text = f" Reason: {reason}" if reason else ""

        # Send a new message to notify about the unmute
        await message.reply_text(f"{user_name} has been unmuted by {admin_name}.{reason_text}")

    except Exception as e:
        # Handle errors
        await message.reply_text(f"Failed to unmute user due to {e}.")


@app.on_message(filters.command(["tmute"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def timed_mute_user(client, message):
    user_id = None  # Initialize user_id
    reason = None  # Initialize reason
    duration = None  # Initialize duration
    try:
        # Check if the message sender is an administrator
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        # Check if the bot itself is an administrator
        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Determine user to mute, duration, and reason
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            args = message.text.split(None, 2)
            if len(args) < 2:
                await message.reply_text("Usage: /tmute <user> <duration> [reason]")
                return

            user_input = args[1]
            duration_input = args[2] if len(args) > 2 else '0s'

            # Extract duration and reason from args
            if ' ' in duration_input:
                duration_part, reason = duration_input.split(' ', 1)
            else:
                duration_part = duration_input

            if user_input.startswith('@'):
                # Handle username
                username = user_input[1:]
                user_id = await resolve_username_to_id(username, client)
                if user_id is None:
                    await message.reply_text("Username not found.")
                    return
            else:
                # Handle user ID
                try:
                    user_id = int(user_input)
                except ValueError:
                    await message.reply_text("Invalid user ID.")
                    return

            # Parse duration
            duration_parts = duration_part.lower().strip()
            if duration_parts.endswith('s'):
                duration = int(duration_parts[:-1])  # seconds
            elif duration_parts.endswith('m'):
                duration = int(duration_parts[:-1]) * 60  # minutes
            elif duration_parts.endswith('h'):
                duration = int(duration_parts[:-1]) * 3600  # hours
            elif duration_parts.endswith('d'):
                duration = int(duration_parts[:-1]) * 86400  # days
            else:
                await message.reply_text("Invalid duration format. Use 's', 'm', 'h', or 'd'.")
                return

            if duration <= 0:
                await message.reply_text("Duration must be greater than zero.")
                return

        if user_id is None:
            await message.reply_text("Please specify a user to mute.")
            return

        # Perform mute
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )

        # Get user and admin info
        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name
        reason_text = f" Reason: {reason}" if reason else ""

        # Send a notification about the mute
        await message.reply_text(f"{user_name} has been muted by {admin_name}.{reason_text} Duration: {duration_part}")

        # Wait for the specified duration and then unmute the user
        await asyncio.sleep(duration)
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True
            )
        )
        await message.reply_text(f"{user_name} has been unmuted after {duration_part}.")

    except FloodWait as e:
        await message.reply_text(f"Too many requests. Please try again later. (Wait {e.x} seconds)")
    except Exception as e:
        await message.reply_text(f"Failed to mute user due to {e}.")


@app.on_message(filters.command(["purge"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def purge(_, ctx: Message):
    try:
        repliedmsg = ctx.reply_to_message
        if not repliedmsg:
            error_msg = await ctx.reply("Reply to the message you want to delete.")
            await asyncio.sleep(4)
            await error_msg.delete()
            return

        # Check if the user is an admin
        chat_id = ctx.chat.id
        user_id = ctx.from_user.id
        chat_member = await _.get_chat_member(chat_id, user_id)
        
        # Debug output to verify the user status
        print(f"User status: {chat_member.status}")

        if chat_member.status not in ['administrator', 'creator']:
            error_msg = await ctx.reply("You must be an admin to use this command.")
            await asyncio.sleep(4)
            await error_msg.delete()
            return

        # Get command arguments
        cmd_args = ctx.command[1:] if len(ctx.command) > 1 else []
        if cmd_args and cmd_args[0].isdigit():
            purge_to = repliedmsg.id + int(cmd_args[0])
            purge_to = min(purge_to, ctx.message.id)
        else:
            purge_to = ctx.message.id

        message_ids = list(range(repliedmsg.id, purge_to + 1))
        del_total = 0

        # Max message deletion limit is 100
        for i in range(0, len(message_ids), 100):
            chunk = message_ids[i:i + 100]
            await _.delete_messages(chat_id=chat_id, message_ids=chunk, revoke=True)
            del_total += len(chunk)

        completion_msg = await ctx.reply("Purge completed.")
        await asyncio.sleep(4)
        await completion_msg.delete()

    except Exception as err:
        error_msg = await ctx.reply(f"ERROR: {err}")
        await asyncio.sleep(5)
        await error_msg.delete()