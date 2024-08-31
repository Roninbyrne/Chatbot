from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter
import asyncio

async def is_admin(user_id: int, chat_id: int, client: Client) -> bool:
    async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            return True
    return False

@app.on_message(filters.group & filters.command("ban"))
async def ban_user(client: Client, message: Message):
    try:
        # Check if the user issuing the command is an admin
        if not await is_admin(message.from_user.id, message.chat.id, client):
            msg = await message.reply("You can't do that. Only admins can use this command.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        # Determine the user to ban
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_mention = message.reply_to_message.from_user.mention
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
                user_mention = f"[User](tg://user?id={user_id})"
            except ValueError:
                msg = await message.reply("Invalid user ID format.")
                await asyncio.sleep(5)
                await msg.delete()
                return
        else:
            msg = await message.reply("Please specify a user to ban.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        # Perform the ban
        await client.ban_chat_member(message.chat.id, user_id)
        msg = await message.reply(f"🚫 Banned {user_mention}.")
        await asyncio.sleep(5)
        await msg.delete()

    except Exception as e:
        msg = await message.reply(f"Failed to ban the user due to: {e}.")
        await asyncio.sleep(5)
        await msg.delete()