from string import Template
import requests
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C
from datetime import datetime


def get_rate():
    """GET request to WazirX api

    Return:
        Fetched Data in json Format
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
    token = update.message.text[:-4].lower()
    tokeninr = token + "inr"
    tokenusd = token + "usdt"
    try:
        rate = get_rate()
        if rate == -1:
            update.message.reply_text(C.OOPS_404)
            return -1
        nratei = rate[tokeninr]['last']
        lratei = rate[tokeninr]['low']
        hratei = rate[tokeninr]['high']
        volumei = rate[tokeninr]['volume']
        timei = datetime.fromtimestamp(
            rate[tokeninr]['at']).strftime('%I:%M:%S %p %d/%m/%Y')
        nrateu = rate[tokenusd]['last']
        lrateu = rate[tokenusd]['low']
        hrateu = rate[tokenusd]['high']
        volumeu = rate[tokenusd]['volume']
        timeu = datetime.fromtimestamp(
            rate[tokenusd]['at']).strftime('%I:%M:%S %p %d/%m/%Y')
    except:
        update.message.reply_text(C.OOPS_404)
        return -1
    rate_text = Template(C.RATE_TEXT_INR).substitute(
        rate=nratei, lrate=lratei, hrate=hratei, vol=volumei, time=timei)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
    rate_text = Template(C.RATE_TEXT_USD).substitute(
        rate=nrateu, lrate=lrateu, hrate=hrateu, vol=volumeu, time=timeu)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
