from string import Template
import datetime
from time import sleep
import requests
import pandas as pd
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C


def get_rate():
    """GET request to WazirX api

    Return:
        last dogecoin price in INR
    """
    try:
        wazirx_request = requests.get('https://api.wazirx.com/api/v2/tickers')
    except:
        print("API Cannot be fetched", file=open(
            C.LOG_FILE, 'a+'))
    if wazirx_request.status_code != 200:
        print('GET /tasks/ {}'.format(wazirx_request.status_code), file=open(
            C.LOG_FILE, 'a+'))
        return -1
    return wazirx_request.json()['dogeinr']['last']


def rate_command(update: Update, context: CallbackContext) -> None:
    """Reply with real time Doge rate

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    rate = get_rate()
    rate_text = Template(C.RATE_TEXT).substitute(rate=rate)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)


def check_status(update: Update, context: CallbackContext) -> int:
    """Checks status if brodcast rate was sent from a specific username,
    and if start command is only invoked once.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    print(f"BRODCAST Rate invoked at: {datetime.datetime.now()}", file=open(
        C.LOG_FILE, 'a+'))
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the person
    username = context.bot.getChatMember(chat_id, user_id).user.username
    if username in ("garvit_joshi9", "pratik_s29"):  # Sent from Developer
        print("Test Case #1: SUCCESS", file=open(C.LOG_FILE, 'a+'))
    else:
        print(f"Test Case #1: FAILED\nUserName: {username}\n", file=open(
            C.LOG_FILE, 'a+'))
        update.message.reply_text(C.ERROR_OWNER,
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        rate_command(update, context)
        return -1
    if C.RATE_FLAG == 0:
        print("Test Case #2: SUCCESS\n", file=open(C.LOG_FILE, 'a+'))
    else:
        print("Test Case #2: FAILED\n", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.ERROR_BRODCAST_AGAIN,
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        rate_command(update, context)
        return -1
    C.RATE_FLAG = 1
    return 0


def plot_rate(update: Update, context: CallbackContext) -> int:
    """Used to plot graph by calling get rate and writing that file into excel sheet (DogeRate.xlsx)

    Keyword arguments:
        update: This object represents an incoming update.
        context: This is a context object error handler.
    """
    if check_status(update, context) == -1:
        return -1
    update.message.reply_text("Rate will be available in a short time",
                              parse_mode=ParseMode.MARKDOWN
                              )
    doge_rate = [[0, 0, 0], [0, 0, 0], [
        0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    while():
        current_rate = get_rate()
        if current_rate == -1:
            update.message.reply_text("A Problem with API has been found, Exiting the function",
                                      parse_mode=ParseMode.MARKDOWN
                                      )
            break
        for i in range(3, -1, -1):
            for j in range(2, -1, -1):
                doge_rate[i+1][j] = doge_rate[i][j]
        date_time = datetime.datetime.now()
        date = date_time.date()
        time = date_time.strftime("%I:%M:%S %p")
        doge_rate[0][0] = current_rate
        doge_rate[0][1] = date
        doge_rate[0][2] = time
        excel_dataframe = pd.DataFrame(doge_rate)
        excel_dataframe.to_excel("DogeRate.xlsx")
        sleep(60)
