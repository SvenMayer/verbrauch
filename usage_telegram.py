#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

import mycredentials


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


NEW_USAGE_CB = None


usage_type = ""

USAGE_KEYS = {"gs": "Gas", "ew": "Etagenwasser", "hw": "Hauptwasser", "st": "Strom"}
USAGE_UNITS = {"Gas": "m³", "Etagenwasser": "m³", "Hauptwasser": "m³", "Strom": "kWh"}
KNOWN_IDS = (mycredentials.mytelegramid, )


def newusage(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    if update.message.chat_id not in KNOWN_IDS:
        return
    keyboard = [
        [
            InlineKeyboardButton("Gas", callback_data='Gas'),
            InlineKeyboardButton("Strom", callback_data='Strom'),
        ],
        [
            InlineKeyboardButton("Hauswasser", callback_data='Hauswasser'),
            InlineKeyboardButton("Etagenwasser", callback_data='Etagenwasser'),
        ],
        [
            InlineKeyboardButton("Abbrechen", callback_data='Cancel'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    global usage_type
    usage_type = query.data
    if query.data == "Cancel":
        query.edit_message_text(text=f"Eingabe abgebrochen")
        usage_type = ""
    else:
        query.edit_message_text(text=f"{query.data}zählerstand eingeben:")


def message(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id not in KNOWN_IDS:
        return
    userinput = update.message.text.strip()
    global usage_type
    if userinput[:1] not in "1234567890":
        if userinput[:2].lower() in USAGE_KEYS.keys():
            usage_type = USAGE_KEYS[userinput[:2].lower()]
            val_str = userinput[2:]
        else:
            update.message.reply_text(text=f"Ungültiger Typ eingeben:")
            return
    elif len(usage_type) > 0:
        try:
            val_str = userinput
        except ValueError:
            update.message.reply_text(text=f"Ungültiger Wert; {usage_type}zählerstand eingeben:")
            return
    else:
        usage_type = ""
        update.message.reply_text(text=f"Kein Typ angegeben.")
        return

    try:
        val = float(val_str)
    except ValueError:
        usage_type = ""
        update.message.reply_text(text=f"Ungültiger Wert für {usage_type}zählerstand eingeben.")
        return
    unit = USAGE_UNITS[usage_type]
    if NEW_USAGE_CB is not None:
        NEW_USAGE_CB(usage_type, val)
        update.message.reply_text(text=f"{usage_type}zählerstand {val} {unit} erfasst")
    usage_type = ""


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(mycredentials.telegram_bot_key)

    updater.dispatcher.add_handler(CommandHandler('newusage', newusage))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
