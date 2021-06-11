from string import Template
from time import sleep
import requests
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C
from datetime import datetime


def alert_plus(update: Update, context: CallbackContext) -> int:
    """Alert when Token increases by ceratin persentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    message = update.message.text
    message = message.split(" ")
    token = str(message[0]+"inr").lower()
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(get_rate()[token]['last'])
    except ValueError:
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        return -1
    except:
        update.message.reply_text(C.OOPS_404)
        return -1
    expected_rate = round(current_rate + (current_rate/100*percentage), 2)
    message_set = Template(C.ALERT_PLUS_SET).substitute(token=token[:-3].upper(
    ), lprice=current_rate, aprice=expected_rate, percentage=percentage)
    update.message.reply_text(message_set, parse_mode=ParseMode.MARKDOWN)
    while True:
        current_rate = float(get_rate()[token]['last'])
        if current_rate >= expected_rate:
            message_executed = Template(C.ALERT_PLUS_EXECUTED).substitute(
                token=token.upper()[:-3], lprice=current_rate, percentage=percentage)
            update.message.reply_text(
                message_executed, parse_mode=ParseMode.MARKDOWN)
            break
        sleep(10)
    return 0


def alert_minus(update: Update, context: CallbackContext) -> int:
    """Alert when Token decreases by ceratin percentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    message = update.message.text
    message = message.split(" ")
    token = str(message[0]+"inr").lower()
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(get_rate()[token]['last'])
    except ValueError:
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        return -1
    except:
        update.message.reply_text(C.OOPS_404)
        return -1
    expected_rate = round(current_rate - (current_rate/100*percentage), 2)
    message_set = Template(C.ALERT_MINUS_SET).substitute(token=token[:-3].upper(
    ), lprice=current_rate, aprice=expected_rate, percentage=percentage)
    update.message.reply_text(message_set, parse_mode=ParseMode.MARKDOWN)
    while True:
        current_rate = float(get_rate()[token]['last'])
        if current_rate <= expected_rate:
            message_executed = Template(C.ALERT_MINUS_EXECUTED).substitute(
                token=token.upper()[:-3], lprice=current_rate, percentage=percentage)
            update.message.reply_text(
                message_executed, parse_mode=ParseMode.MARKDOWN)
            break
        sleep(10)
    return 0


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


def rate_command(update: Update, context: CallbackContext, token=None) -> int:
    """Reply with real time Token rate

    Keyword arguments:
        update: This object represents an incoming update.
        context: This is a context object error handler.
    """
    if token == None:
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
        token=token.upper(), rate=nratei, lrate=lratei, hrate=hratei, vol=volumei, time=timei)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
    rate_text = Template(C.RATE_TEXT_USD).substitute(
        token=token.upper(), rate=nrateu, lrate=lrateu, hrate=hrateu, vol=volumeu, time=timeu)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)


def all_rate(update: Update, context: CallbackContext) -> int:
    try:
        rate = get_rate()
    except:
        update.message.reply_text(C.OOPS_404)
        return -1
    inrtokens = ["btc", "matic", "eth", "hbar",
                 "doge", "xrp", "ada", "xlm", "link", "trx"]
    usdttokens = ["btc", "matic", "eth", "hbar",
                  "doge", "xrp", "ada", "xlm", "link", "trx", "xmr", "theta", "tfuel"]
    message = ""
    for token in inrtokens:
        tokeninr = token + "inr"
        token_rate = rate[tokeninr]['last']
        message = message + token.upper() + ": " + token_rate + " INR\n"
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    message = ""
    for token in usdttokens:
        tokenusdt = token + "usdt"
        token_rate = rate[tokenusdt]['last']
        message = message + token.upper() + ": " + token_rate + " USDT\n"
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
