import asyncio
import datetime
from pyrogram import filters, enums, Client
from pyrogram.types import ChatPermissions, Message
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, BadRequest
from pyrogram.errors import UserNotParticipant
from AnonXMusic import app

def mention(user_id, name, mention=True):
    if mention:
        return f"[{name}](tg://openmessage?user_id={user_id})"
    return f"[{name}](https://t.me/{user_id})"

async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
        return [user.id, user.first_name]
    except:
        return None

async def ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, time=None):
    try:
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "You need to be an admin to perform this action.", False
    except UserAdminInvalid:
        return "The user is an admin and cannot be banned.", False
    except Exception as e:
        if user_id == app.id:
            return "I cannot ban myself.", False
        return f"An error occurred: {str(e)}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    msg_text = f"{user_mention} has been banned by {admin_mention}.\n"
    if reason:
        msg_text += f"Reason: `{reason}`\n"
    if time:
        msg_text += f"Duration: `{time}`\n"
    return msg_text, True

async def unban_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "You need to be an admin to perform this action.", False
    except Exception as e:
        return f"An error occurred: {str(e)}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    return f"{user_mention} has been unbanned by {admin_mention}.", True

async def mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason, time=None):
    try:
        permissions = ChatPermissions()
        if time:
            mute_end_time = datetime.datetime.now() + time
            await app.restrict_chat_member(chat_id, user_id, permissions, until_date=mute_end_time)
        else:
            await app.restrict_chat_member(chat_id, user_id, permissions)
    except ChatAdminRequired:
        return "You need to be an admin to perform this action.", False
    except UserAdminInvalid:
        return "The user is an admin and cannot be muted.", False
    except Exception as e:
        if user_id == app.id:
            return "I cannot mute myself.", False
        return f"An error occurred: {str(e)}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    msg_text = f"{user_mention} has been muted by {admin_mention}.\n"
    if reason:
        msg_text += f"Reason: `{reason}`\n"
    if time:
        msg_text += f"Duration: `{time}`\n"
    return msg_text, True

async def unmute_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_media_messages=True,
                can_send_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )
    except ChatAdminRequired:
        return "You need to be an admin to perform this action.", False
    except Exception as e:
        return f"An error occurred: {str(e)}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    return f"{user_mention} has been unmuted by {admin_mention}.", True

async def delete_message_after_delay(message, delay=5):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {str(e)}")

@app.on_message(filters.command(["ban"]))
async def ban_command_handler(client: Client, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name

    try:
        member = await chat.get_member(admin_id)
    except Exception as e:
        response = f"An error occurred: {str(e)}"
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        response = "You don't have permission to ban users."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    if not member.privileges.can_restrict_members:
        response = "You don't have the required privileges to ban users."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    user_id, first_name, reason = None, None, None
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            reason = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else None
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
                reason = message.text.partition(message.command[1])[2].strip() or None
            except ValueError:
                try:
                    user_obj = await get_userid_from_username(message.command[1])
                    if user_obj is None:
                        response = "I can't find that user."
                        reply = await message.reply_text(response)
                        await delete_message_after_delay(reply)
                        return
                    user_id, first_name = user_obj
                    reason = message.text.partition(message.command[1])[2].strip() or None
                except Exception as e:
                    response = f"An error occurred: {str(e)}"
                    reply = await message.reply_text(response)
                    await delete_message_after_delay(reply)
                    return
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        response = "Please specify a valid user or reply to a message."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    try:
        msg_text, result = await ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason)
        reply = await message.reply_text(msg_text)
        await delete_message_after_delay(reply)
    except ChatAdminRequired:
        response = "You must have admin permissions to ban users."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
    except UserNotParticipant:
        response = "The user is not a participant in this chat."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
    except Exception as e:
        response = f"An error occurred: {str(e)}"
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)

@app.on_message(filters.command(["unban"]))
async def unban_command_handler(client: Client, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name

    try:
        member = await chat.get_member(admin_id)
    except Exception as e:
        response = f"An error occurred: {str(e)}"
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        response = "You don't have permission to unban users."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    if not member.privileges.can_restrict_members:
        response = "You don't have the required privileges to unban users."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    user_id, first_name = None, None
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except ValueError:
            try:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj is None:
                    response = "I can't find that user."
                    reply = await message.reply_text(response)
                    await delete_message_after_delay(reply)
                    return
                user_id, first_name = user_obj
            except Exception as e:
                response = f"An error occurred: {str(e)}"
                reply = await message.reply_text(response)
                await delete_message_after_delay(reply)
                return
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        response = "Please specify a valid user or reply to a message."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
        return

    try:
        msg_text, result = await unban_user(user_id, first_name, admin_id, admin_name, chat_id)
        reply = await message.reply_text(msg_text)
        await delete_message_after_delay(reply)
    except ChatAdminRequired:
        response = "You must have admin permissions to unban users."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
    except UserNotParticipant:
        response = "The user is not a participant in this chat."
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)
    except Exception as e:
        response = f"An error occurred: {str(e)}"
        reply = await message.reply_text(response)
        await delete_message_after_delay(reply)



@app.on_message(filters.command(["mute"]))
async def mute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ ꜱᴏᴍᴇᴏɴᴇ"
            return await message.reply_text(msg_text)
    else:
        msg_text = "ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ ꜱᴏᴍᴇᴏɴᴇ"
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            reason = message.text.split(None, 1)[1]
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                reason = message.text.partition(message.command[1])[2]
            except:
                reason = None

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = None
    else:
        await message.reply_text("ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ")
        return

    msg_text, result = await mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason)
    if result == True:
        await message.reply_text(msg_text)

    if result == False:
        await message.reply_text(msg_text)


@app.on_message(filters.command(["unmute"]))
async def unmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ ꜱᴏᴍᴇᴏɴᴇ"
            return await message.reply_text(msg_text)
    else:
        msg_text = "ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ ꜱᴏᴍᴇᴏɴᴇ"
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj == None:
                    return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ")
            user_id = user_obj[0]
            first_name = user_obj[1]

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        await message.reply_text("ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ")
        return

    msg_text = await unmute_user(user_id, first_name, admin_id, admin_name, chat_id)
    await message.reply_text(msg_text)





@app.on_message(filters.command(["tmute"]))
async def tmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ ꜱᴏᴍᴇᴏɴᴇ"
            return await message.reply_text(msg_text)
    else:
        msg_text = "ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ ꜱᴏᴍᴇᴏɴᴇ"
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            time = message.text.split(None, 1)[1]

            try:
                time_amount = time.split(time[-1])[0]
                time_amount = int(time_amount)
            except:
                return await message.reply_text("ᴡʀᴏɴɢ ꜰᴏʀᴍᴀᴛ!!\n ꜰᴏʀᴍᴀᴛ : `/tmute 2m`")

            if time[-1] == "m":
                mute_duration = datetime.timedelta(minutes=time_amount)
            elif time[-1] == "h":
                mute_duration = datetime.timedelta(hours=time_amount)
            elif time[-1] == "d":
                mute_duration = datetime.timedelta(days=time_amount)
            else:
                return await message.reply_text("ᴡʀᴏɴɢ ꜰᴏʀᴍᴀᴛ!!\n ꜰᴏʀᴍᴀᴛ :\nm: Minutes\nh: Hours\nd: Days")
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                time = message.text.partition(message.command[1])[2]
                try:
                    time_amount = time.split(time[-1])[0]
                    time_amount = int(time_amount)
                except:
                    return await message.reply_text("ᴡʀᴏɴɢ ꜰᴏʀᴍᴀᴛ!!\n ꜰᴏʀᴍᴀᴛ : `/tmute 2m`")

                if time[-1] == "m":
                    mute_duration = datetime.timedelta(minutes=time_amount)
                elif time[-1] == "h":
                    mute_duration = datetime.timedelta(hours=time_amount)
                elif time[-1] == "d":
                    mute_duration = datetime.timedelta(days=time_amount)
                else:
                    return await message.reply_text("ᴡʀᴏɴɢ ꜰᴏʀᴍᴀᴛ!!\n ꜰᴏʀᴍᴀᴛ :\nm: Minutes\nh: Hours\nd: Days")
            except:
                return await message.reply_text("ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ\n ꜰᴏʀᴍᴀᴛ : `/tmute @user 2m`")

    else:
        await message.reply_text("ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ\n ꜰᴏʀᴍᴀᴛ: /tmute <username> <time>")
        return

    msg_text, result = await mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason=None, time=mute_duration)
    if result == True:
        await message.reply_text(msg_text)
    if result == False:
        await message.reply_text(msg_text)