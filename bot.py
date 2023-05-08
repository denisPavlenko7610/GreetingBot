#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

from datetime import datetime, timezone
from threading import Timer
import logging
import ctypes
import random
from array import *
from typing import Tuple, Optional
import os
import datetime
from datetime import timedelta
PORT = int(os.environ.get('PORT', 5000))
TOKEN = '5067045905:AAGlU49fTtkU8HG44zir3zcMjagzqMUl8Wo'
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
lib = ctypes.windll.kernel32


from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def extract_status_change(
    chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = (
        old_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )
    is_member = (
        new_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member


def track_chats(update: Update, context: CallbackContext) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            logger.info("%s started the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    else:
        if not was_member and is_member:
            logger.info("%s added the bot to the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


def show_chats(update: Update, context: CallbackContext) -> None:
    """Shows which chats the bot is in"""
    user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
    group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
    channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
    text = (
        f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
        f" Moreover it is a member of the groups with IDs {group_ids} "
        f"and administrator in the channels with IDs {channel_ids}."
    )
    update.effective_message.reply_text(text)


def greet_chat_members(update: Update, context: CallbackContext) -> None:
    """Greets new users in chats"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    game_emoji = ["🎮","🎮","🎮","🕹","🎾","👾","🌍","🌐","🏝","🛰","🛸","🚀","🔥","⚽","🀄","🎨","⛑","🎵","🎧","📻","🎹","🎻","🎺","🎸","🥁","📱","💻","🔷","🖥","🖱","💿","💾","🎥","🎬","📖","💰","💸","✉","📫","💼","🔭","📡","🔬"]
    smile_first_emoji = ["😄","😀","😃","😁","🤠", "👻","😺","🎅","🐶","🐮","🐘","🐧","🐋","🐙","🦠","🤩","🤯"]
    smile_second_emoji = ["🙂","😉","🤠","😎","🤓","👽","👽","👨‍💻","🥷","🥷","🤴","👳‍♂️","🧙","🧛‍♂️","🧝","🧞‍♂️","🦄","🐭","🐰","🐌","🗿","☣","☯"]
    rangom_game_num = random.randint(1, len(game_emoji) - 1)
    rangom_smile_first_num = random.randint(1, len(smile_first_emoji) - 1)
    rangom_smile_second_num = random.randint(1, len(smile_second_emoji) - 1)

    start_time = lib.GetTickCount64()
    start_time = int(str(start_time)[:-3])
    mins, sec = divmod(start_time, 60)

    #now_hours = int(datetime.datetime.now().strftime("%H"))
    if mins < 10:
        print(mins)
        was_member, is_member = result
    else:
        print(mins)
        was_member, is_member = result
        member_name = update.chat_member.new_chat_member.user.mention_html()
        if not was_member and is_member:
            update.effective_chat.send_message(
                f"Привет, {member_name} {smile_first_emoji[rangom_smile_first_num]}. В этой группе ты можешь делиться чем-то интересным из мира айти, задавать вопросы и также помогать другим) {game_emoji[rangom_game_num]} Вверху прикреплены материалы которые тебе, возможно, будут интересны. Welcome! {smile_second_emoji[rangom_smile_second_num]}",
                parse_mode=ParseMode.HTML)


def main() -> None:
    """Start Welcome bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Keep track of which chats the bot is in
    dispatcher.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(CommandHandler("show_chats", show_chats))

    # Handle members joining/leaving chats.
    dispatcher.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Start the Bot
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    updater.start_polling(allowed_updates=Update.CHAT_JOIN_REQUEST)
     # Start the Bot
    #updater.start_webhook(listen="0.0.0.0",
    #                      port=int(PORT),
    #                      url_path=TOKEN)
    #updater.bot.setWebhook('https://rdragon-hello.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()