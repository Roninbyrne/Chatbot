from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from AnonXMusic import app  # Importing the app object from your project

async def get_admin_permissions(admin_id, chat_id):
    """Get the permissions of the admin."""
    admin = await app.get_chat_member(chat_id, admin_id)
    permissions = admin.privileges
    return permissions

async def promote_user_with_admin_permissions(client, chat_id, user_id, admin_permissions):
    """Promote a user with permissions the admin has."""
    await client.promote_chat_member(
        chat_id,
        user_id,
        can_change_info=admin_permissions.can_change_info,
        can_post_messages=admin_permissions.can_post_messages,
        can_edit_messages=admin_permissions.can_edit_messages,
        can_delete_messages=admin_permissions.can_delete_messages,
        can_invite_users=admin_permissions.can_invite_users,
        can_restrict_members=admin_permissions.can_restrict_members,
        can_pin_messages=admin_permissions.can_pin_messages,
        can_promote_members=admin_permissions.can_promote_members
    )

@app.on_message(filters.command(["promote"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def promote_user(client, message):
    user_id = None
    try:
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Get the permissions of the admin
        admin_permissions = await get_admin_permissions(message.from_user.id, message.chat.id)

        if not admin_permissions.can_promote_members:
            await message.reply_text("You don't have permission to promote users.")
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                await message.reply_text("Invalid user ID.")
                return

        if user_id is None:
            await message.reply_text("Please specify a user to promote.")
            return

        # Promote user with the admin's permissions
        await promote_user_with_admin_permissions(client, message.chat.id, user_id, admin_permissions)

        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name

        await message.reply_text(f"{user_name} has been promoted by {admin_name}.")

    except Exception as e:
        await message.reply_text(f"Failed to promote user due to {e}.")

@app.on_message(filters.command(["fullpromote"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def fullpromote_user(client, message):
    user_id = None
    try:
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Get the permissions of the admin
        admin_permissions = await get_admin_permissions(message.from_user.id, message.chat.id)

        if not admin_permissions.can_promote_members:
            await message.reply_text("You don't have permission to fully promote users.")
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                await message.reply_text("Invalid user ID.")
                return

        if user_id is None:
            await message.reply_text("Please specify a user to fully promote.")
            return

        # Full promote user with the admin's permissions
        await promote_user_with_admin_permissions(client, message.chat.id, user_id, admin_permissions)

        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name

        await message.reply_text(f"{user_name} has been fully promoted by {admin_name}.")

    except Exception as e:
        await message.reply_text(f"Failed to fully promote user due to {e}.")

@app.on_message(filters.command(["lowpromote"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def lowpromote_user(client, message):
    user_id = None
    try:
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Get the permissions of the admin
        admin_permissions = await get_admin_permissions(message.from_user.id, message.chat.id)

        if not admin_permissions.can_promote_members:
            await message.reply_text("You don't have permission to low promote users.")
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                await message.reply_text("Invalid user ID.")
                return

        if user_id is None:
            await message.reply_text("Please specify a user to low promote.")
            return

        # Low promote user with the admin's permissions
        await promote_user_with_admin_permissions(client, message.chat.id, user_id, admin_permissions)

        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name

        await message.reply_text(f"{user_name} has been low promoted by {admin_name}.")

    except Exception as e:
        await message.reply_text(f"Failed to low promote user due to {e}.")

@app.on_message(filters.command(["demote"], prefixes=["/", "!"]) & (filters.group | filters.channel))
async def demote_user(client, message):
    user_id = None
    try:
        if not await is_administrator(message.from_user.id, message, client):
            await message.reply_text("You can't do that.")
            return

        if not await is_bot_administrator(message, client):
            await message.reply_text("I need to be an administrator to perform this action.")
            return

        # Get the permissions of the admin
        admin_permissions = await get_admin_permissions(message.from_user.id, message.chat.id)

        if not admin_permissions.can_promote_members:
            await message.reply_text("You don't have permission to demote users.")
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                await message.reply_text("Invalid user ID.")
                return

        if user_id is None:
            await message.reply_text("Please specify a user to demote.")
            return

        # Demote user with the admin's permissions
        await promote_user_with_admin_permissions(client, message.chat.id, user_id, admin_permissions)

        user = await client.get_users(user_id)
        admin_name = message.from_user.first_name
        user_name = user.first_name

        await message.reply_text(f"{user_name} has been demoted by {admin_name}.")

    except Exception as e:
        await message.reply_text(f"Failed to demote user due to {e}.")