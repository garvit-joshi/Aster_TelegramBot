from string import Template
import re
from time import sleep
import configparser
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from telegram import Update, ParseMode
import constants as C
import rate as R
from threading import Thread, Event


print("Bot Started...\n")
log_text = f"Bot Started at {R.get_time()}\n"
log_text = log_text + f"Initializing tasks\n"
R.print_logs(log_text)


def welcome_user(update: Update, context: CallbackContext) -> None:
    """Welcome Command for New User
    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    for new_user in update.message.new_chat_members:
        chat_id = update.message.chat_id
        new_user = new_user.first_name
        welcome_message = "Welcome " + new_user
        context.bot.send_message(chat_id, welcome_message)
        log_text = f"Welcome user at {R.get_time()} \nUser: {R.get_username(update, context)}\n"
        R.print_logs(log_text)


def start_command(update: Update, context: CallbackContext) -> None:
    """Start Command for Aster
    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    user = update.message.from_user
    update.message.reply_text(f'Hy there !! {user.first_name}')


def help_command(update: Update, context: CallbackContext) -> None:
    """Help Command for User
    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    update.message.reply_text(C.HELP_TEXT, parse_mode=ParseMode.MARKDOWN)


def source_command(update: Update, context: CallbackContext) -> None:
    """Prints GitHub Source Code
    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    username = update.message.from_user.first_name
    message = Template(C.SOURCE).substitute(name=username)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def send_logs(update: Update, context: CallbackContext) -> None:
    """Sends Logs
    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    chat_id = update.message.chat_id
    username = R.get_username(update, context)
    log_text = "Command: Get Logs\n"
    log_text = log_text + f"Time: {R.get_time(update)}\n"
    log_text = log_text + f"User: {username}\n"
    if username == "garvit_joshi9":  # Sent from Developer
        try:
            with open(C.LOG_FILE, "rb") as file:
                context.bot.send_document(
                    chat_id=chat_id, document=file, filename=C.LOG_FILE)
        except Exception as e:
            log_text = log_text + f"Remarks: Error with File logs\n"
            log_text = log_text + f"{e}\n"
            update.message.reply_text("Error with logs file.")
    else:
        log_text = log_text + f"Remarks: Not a Developer\n"
        update.message.reply_text(C.ERROR_PRIVILEGE)
    R.print_logs(log_text)


def rate_runner():
    """Runs get_rate after every 5 sec.
    """
    log_text = f"Deamon Thread Initialized...\n"
    R.print_logs(log_text)
    while True:
        R.get_rate()
        sleep(3)


def main():
    """Main function responsible for starting the bot and listening to commands.
    """
    config = configparser.ConfigParser()
    config.read('secrets.ini')

    # Create the Updater and pass it our bot's token.
    updater = Updater(token=config['KEYS']
                      ['API_KEY'], use_context=True, workers=C.WORKERS)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome_user))
    dispatch.add_handler(CommandHandler("start", start_command))
    dispatch.add_handler(MessageHandler(Filters.regex(
        re.compile('RATE$', re.IGNORECASE)), R.rate_command, run_async=True))
    dispatch.add_handler(MessageHandler(
        Filters.regex(r'\+-$'), R.alert_plus_minus, run_async=True))
    dispatch.add_handler(MessageHandler(
        Filters.regex(r'\+$'), R.alert_plus, run_async=True))
    dispatch.add_handler(MessageHandler(
        Filters.regex(r'-$'), R.alert_minus, run_async=True))
    dispatch.add_handler(CommandHandler("source", source_command))
    dispatch.add_handler(CommandHandler(
        "cancel_alerts", R.cancel_alert, run_async=True))
    dispatch.add_handler(CommandHandler("all_rates", R.all_rate))
    dispatch.add_handler(CommandHandler("help", help_command))
    dispatch.add_handler(CommandHandler(
        "get_logs", send_logs, run_async=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    rate_updater = Thread(target=rate_runner, daemon=True)
    rate_updater.start()
    main()
