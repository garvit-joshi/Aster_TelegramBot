from string import Template
from time import sleep
import requests
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C


def get_rate():
    """GET request to WazirX api

    Return:
        Fetched Data
    """
    try:
        wazirx_request = requests.get('https://api.wazirx.com/api/v2/tickers')
    except:
        print("API Cannot be fetched", file=open(
            C.LOG_FILE, 'a+'))
        return -1
    if wazirx_request.status_code != 200:
        print('GET /tasks/ {}'.format(wazirx_request.status_code), file=open(
            C.LOG_FILE, 'a+'))
        return -1
    return wazirx_request.json()


def rate_command(update: Update, context: CallbackContext) -> None:
    """Reply with real time Token rate

    Keyword arguments:
        update: This object represents an incoming update.
        context: This is a context object error handler.
    """
    token = update.message.text
    try:
        rate = get_rate()
        if rate == -1:
            update.message.reply_text(C.OOPS_404)
            return -1
        rate = rate[token]['last']
    except:
        update.message.reply_text("No Token Found with this name")
    rate_text = Template(C.RATE_TEXT).substitute(rate=rate)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
