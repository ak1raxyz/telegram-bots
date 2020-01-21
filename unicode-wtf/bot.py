
import os
import uuid
import logging

import telegram

from flask import Flask, request
from telegram import Update, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import (
    Updater, CallbackContext, CommandHandler, MessageHandler, InlineQueryHandler, Filters
)

from utils import get_logger, charecter_maps, unicode_conv

# Enable logging
logger = get_logger(__name__)

# Initial bot by Telegram access token
token = os.environ.get("ACCESS_TOKEN")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# Initial Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route("/%s/hook" % token, methods=["POST"])
def webhook():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
        dispatcher.process_update(update)
    return "ok"

def start_handler(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    reply = "Convert input ASCII texts to Unicode."
    update.message.reply_text(reply)

def echo_handler(update: Update, context: CallbackContext):
    if not update.message.text:
        return
    reply = unicode_conv(update.message.text)
    if update.message.chat.type == "private":
        update.message.reply_text(reply)

def error_handler(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning("Update '%s' caused error '%s'", update, context.error)
    update.message.reply_text("Something badly happend, please try again later.")

def inline_query_handler(update: Update, context: CallbackContext):
    query = update.inline_query.query
    logger.info("telegram.InlineQuery: '%s' triggered..." % query)
    message_list = list()
    if not query:
        return
    for style in charecter_maps.keys():
        converted_query = unicode_conv(query, style=style)
        message = InlineQueryResultArticle(
            id=uuid.uuid4(),
            title=style,
            description=converted_query,
            input_message_content=InputTextMessageContent(
                message_text=converted_query
            )
        )
        message_list.append(message)
    update.inline_query.answer(message_list)

# Add handlers for handling message.
dispatcher.add_handler(CommandHandler("start", start_handler))
dispatcher.add_handler(InlineQueryHandler(inline_query_handler))
dispatcher.add_handler(MessageHandler(Filters.text, echo_handler))
dispatcher.add_error_handler(error_handler)

if __name__ == "__main__":
    app.run(debug=False)
