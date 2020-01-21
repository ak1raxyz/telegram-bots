
import os
import json
import uuid
import random
import logging

import telegram
from flask import Flask, request
from telegram import (
    InputTextMessageContent,
    InlineQueryResultVoice, InlineQueryResultCachedVoice
)
from telegram.ext import (
    Dispatcher, CommandHandler, MessageHandler, InlineQueryHandler, Filters
)

# Load data from environment varibles
token = os.environ.get("ACCESS_TOKEN")
voice_base_url = os.environ.get("VOICE_BASE_URL")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Prepare voice assert for voice_handler
voice_assert = "assets/voice"
voice_conf_file = "assets/voice.json"
with open(voice_conf_file) as f:
    voice_conf = json.loads(f.read())

welcome_message = '''
Hello, I am HAL 9000, the Next Generation, I can do many thing for you.

Type /help for detail.
'''

help_message = '''
Hello, I am HAL 9000, the Next Generation, Hope you have fun here.

/help - Show this help message.
/cantdo - "I'm sorry Dave, I'm afraid I can't do that."
/quote - Return 5 random quote text from HAL 9000.
/random - Return a random quote with voice from HAL 9000.
Inline mode - Type keywords to search quote from HAL 9000.
'''

# Initial bot by Telegram access token
bot = telegram.Bot(token=token)

# Initial Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return welcome_message

@app.route("/hook", methods=["POST"])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"

def start_handler(bot, update):
    """Send a message when the command /start is issued."""
    reply = welcome_message
    if update.message.chat.type == "private":
        update.message.reply_text(reply)

def help_handler(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_message)

def reply_handler(bot, update):
    """Reply message."""
    reply = update.message.text
    if update.message.chat.type == "private":
        update.message.reply_text(reply)

def error_handler(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error("Update '%s' caused error '%s'" % (update, error))
    update.message.reply_text(help_message)

# custom handlers
def send_voice(bot, update, reply):
    """Send message helper function."""
    chat_id = update.message.chat_id
    file_id = reply.get("file_id")
    if file_id:
        message = bot.send_voice(chat_id=chat_id, voice=file_id, caption=reply.get("text"))
    else:
        with open(os.path.join(voice_assert, reply.get("file")), "rb") as voice:
            message = bot.send_voice(chat_id=chat_id, voice=voice, caption=reply.get("text"))

        file_id = message.voice.file_id
        logger.info("Message:telegram.Message send First time, save file_id:%s to %s" % (file_id, voice_conf_file))
        global voice_conf
        for voice in voice_conf:
            if voice.get("id") == reply.get("id"):
                voice["file_id"] = file_id
        with open(voice_conf_file, "w") as f:
            f.write(json.dumps(voice_conf, indent=2))

    logger.info("Message:telegram.Message '%s' sent as voice." % message)

def voice_list_handler(bot, update):
    """Return 5 random voice text."""
    voice_all = [q.get("text") for q in voice_conf]
    random.shuffle(voice_all)
    reply = "\n".join(voice_all[:5])
    update.message.reply_text(reply)

def cantdo_handler(bot, update):
    """Return Let the bass kick."""
    for voice in voice_conf:
        if voice.get("id") == "cantdo":
            reply = voice
    send_voice(bot, update, reply)

def voice_handler(bot, update):
    """Return a random voice with voice."""
    voice_shuffle = voice_conf[:]
    random.shuffle(voice_shuffle)
    reply = voice_shuffle[-1]
    send_voice(bot, update, reply)

def inline_voice_handler(bot, update):
    query = update.inline_query.query
    logger.info("telegram.InlineQuery: '%s' triggered..." % query)
    voice_list = list()
    for voice in voice_conf:
        if query in voice.get("text"):
            voice_list.append(voice)
    results = list()
    for voice in voice_list:
        file_id = voice.get("file_id")
        if file_id:
            message = InlineQueryResultCachedVoice(
                id=uuid.uuid4(), title=voice.get("text"), description=voice.get("text"),
                voice_file_id=file_id, caption=voice.get("text")
            )
        else:
            message = InlineQueryResultVoice(
                id=uuid.uuid4(), title=voice.get("text"), description=voice.get("text"),
                voice_url=voice_base_url+voice.get("file"), caption=voice.get("text")
            )
        logger.info("Message:telegram.InlineQueryResult '%s' appended to results." % message)
        results.append(message)
    update.inline_query.answer(results)

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handlers for handling message.
dispatcher.add_handler(CommandHandler("start", start_handler))
dispatcher.add_handler(CommandHandler("help", help_handler))

dispatcher.add_handler(CommandHandler("quote", voice_list_handler))
dispatcher.add_handler(CommandHandler("random", voice_handler))
dispatcher.add_handler(CommandHandler("cantdo", cantdo_handler))
dispatcher.add_handler(InlineQueryHandler(inline_voice_handler))
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_error_handler(error_handler)

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
