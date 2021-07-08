from string import Template
import re
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


print("\n\n\n", file=open(C.LOG_FILE, 'a+'))
R.print_line()
R.print_line()
print("Bot Started...\n")
print(f"Bot Started at {R.get_time()}\n", file=open(C.LOG_FILE, 'a+'))


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
        R.print_line()
        print(f"Welcome user at {R.get_time()} \nUser: {R.get_username(update, context)}", file=open(
            C.LOG_FILE, 'a+'))


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


def main():
    """Main function responsible for starting the bot and listening to commands.
    """
    config = configparser.ConfigParser()
    config.read('secrets.ini')

    # Create the Updater and pass it our bot's token.
    updater = Updater(token=config['KEYS']['API_KEY'], use_context=True, workers=8)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome_user))
    dispatch.add_handler(CommandHandler("start", start_command))
    dispatch.add_handler(MessageHandler(Filters.regex(
        re.compile('RATE$', re.IGNORECASE)), R.rate_command, run_async=True))
    dispatch.add_handler(MessageHandler(
        Filters.regex(r'\+$'), R.alert_plus, run_async=True))
    dispatch.add_handler(MessageHandler(
        Filters.regex(r'-$'), R.alert_minus, run_async=True))
    dispatch.add_handler(CommandHandler("source", source_command))
    dispatch.add_handler(CommandHandler(
        "cancel_alerts", R.cancel_alert, run_async=True))
    dispatch.add_handler(CommandHandler("all_rates", R.all_rate))
    dispatch.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
