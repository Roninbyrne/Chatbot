import asyncio
from AnonXMusic import app
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import Message
from os import environ

# Dictionary to store the status of safety checks per chat
safety_status = {}
# Dictionary to store the exception list per chat
exception_list = {}

# Function to get admin user IDs
async def get_admins(client: Client, chat_id: int):
    admins = []
    async for member in client.get_chat_members(chat_id, filter="administrators"):
        admins.append(member.user.id)
    return admins

# Command to enable or disable safety checks
@app.on_message(filters.group & filters.command("safety"))
async def handle_safety_command(client: Client, message: Message):
    admins = await get_admins(client, message.chat.id)

    if message.from_user.id not in admins:
        await message.reply("You do not have permission to use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        await message.reply("Usage: /safety <enable/disable>")
        return

    action = command[1].lower()
    chat_id = message.chat.id

    if action not in ["enable", "disable"]:
        await message.reply("Invalid action. Use 'enable' or 'disable'.")
        return

    safety_status[chat_id] = (action == "enable")
    status = "enabled" if action == "enable" else "disabled"

    response_message = await message.reply(f"Safety checks have been {status} for this group.")
    await asyncio.sleep(5)
    await response_message.delete()

# Command to add users to the exception list
@app.on_message(filters.group & filters.command("free"))
async def handle_free_command(client: Client, message: Message):
    admins = await get_admins(client, message.chat.id)

    if message.from_user.id not in admins:
        await message.reply("You do not have permission to use this command.")
        return

    command = message.text.split()
    if len(command) < 2:
        await message.reply("Usage: /free <user_id or username>")
        return

    user_input = command[1]
    chat_id = message.chat.id

    # Try to convert input to user ID
    user_id = None
    user_first_name = None
    try:
        user_id = int(user_input)
    except ValueError:
        # Handle username if necessary
        async for member in client.get_chat_members(chat_id):
            if member.user.username == user_input:
                user_id = member.user.id
                user_first_name = member.user.first_name
                break
    else:
        # Get user information by ID
        user = await client.get_users(user_id)
        user_first_name = user.first_name

    if user_id is None:
        response_message = await message.reply("Invalid user ID or username.")
        await asyncio.sleep(5)
        await response_message.delete()
        return

    if chat_id not in exception_list:
        exception_list[chat_id] = set()

    exception_list[chat_id].add(user_id)

    admin_first_name = message.from_user.first_name
    if user_first_name is None:
        user = await client.get_users(user_id)
        user_first_name = user.first_name

    # Notify the group
    notification = f"{user_first_name} has been added to the exception list by {admin_first_name}."
    response_message = await message.reply(notification)
    await asyncio.sleep(5)
    await response_message.delete()

# Command to list users in the exception list
@app.on_message(filters.group & filters.command("freelist"))
async def handle_freelist_command(client: Client, message: Message):
    admins = await get_admins(client, message.chat.id)

    if message.from_user.id not in admins:
        await message.reply("You do not have permission to use this command.")
        return

    chat_id = message.chat.id

    if chat_id not in exception_list or not exception_list[chat_id]:
        response_message = await message.reply("The exception list is currently empty.")
        await asyncio.sleep(5)
        await response_message.delete()
        return

    # Fetch exception list user details
    exception_users = exception_list[chat_id]
    user_details = []

    for user_id in exception_users:
        try:
            user = await client.get_users(user_id)
            user_details.append(f"{user.first_name} (ID: {user_id})")
        except RPCError as e:
            print(e)

    # Create a message with the list of users
    if user_details:
        exception_list_message = "Exception List:\n" + "\n".join(user_details)
    else:
        exception_list_message = "The exception list is empty or could not fetch user details."

    response_message = await message.reply(exception_list_message)
    await asyncio.sleep(5)
    await response_message.delete()

@app.on_message()
async def handle_message(client: Client, message: Message):
    chat_id = message.chat.id

    # Ensure safety checks are enabled by default if not explicitly set
    if not safety_status.get(chat_id, True):
        return  # Safety checks are disabled; do nothing

    # Check if the message is edited
    if message.edit_date:
        # Check if the user is in the exception list
        user_id = message.from_user.id
        if chat_id in exception_list and user_id in exception_list[chat_id]:
            return  # User is exempt from safety checks

        # Check if the bot has permission to delete messages
        chat_member = await client.get_chat_member(chat_id, client.me.id)
        can_delete = "can_delete_messages" in chat_member.privileges

        user = message.from_user
        user_name = user.first_name

        # Check if the edited message contains a file or PDF
        if message.document:
            try:
                if can_delete:
                    await message.delete()
                    response = f"{user_name} tried to pull copyright module so I deleted it."
                else:
                    response = f"{user_name} tried to pull copyright module but I don't have permission to delete it."
            except RPCError as e:
                print(e)
            response_message = await client.send_message(chat_id=chat_id, text=response)
            await asyncio.sleep(5)
            await response_message.delete()
            return

        # Check if the edited message contains more than 200 words
        message_text = message.text or ""
        if len(message_text.split()) > 200:
            try:
                if can_delete:
                    await message.delete()
                    response = f"{user_name} tried to pull copyright module so I deleted it."
                else:
                    response = f"{user_name} tried to pull copyright module but I don't have permission to delete it."
            except RPCError as e:
                print(e)
            response_message = await client.send_message(chat_id=chat_id, text=response)
            await asyncio.sleep(5)
            await response_message.delete()
            return

        # Handle other edited messages
        try:
            if can_delete:
                await message.delete()
                response = f"{user_name} tried to edit messages and I deleted it."
            else:
                response = f"{user_name} edited the message but I don't have permission to delete it."
        except RPCError as e:
            print(e)

        response_message = await client.send_message(chat_id=chat_id, text=response)
        await asyncio.sleep(5)
        await response_message.delete()