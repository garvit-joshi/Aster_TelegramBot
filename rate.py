from string import Template
from time import sleep
from datetime import datetime
import requests
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C


def get_time():
    """Gets Current Time

    Returns:
        HH:MM:SS AM/PM DD/MM/YYYY
    """
    return datetime.now().strftime('%I:%M:%S %p %d/%m/%Y')


def get_username(update: Update, context: CallbackContext):
    """Gets Username of a person

    Returns:
        username
    """
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the person
    username = context.bot.getChatMember(chat_id, user_id).user.username
    return username


def print_line():
    """Writes a small line seperator in logs.txt
    """
    print("-------------", file=open(C.LOG_FILE, 'a+'))


def alert_plus(update: Update, context: CallbackContext) -> int:
    """Alert when Token increases by ceratin persentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    C.ALERT_COUNT = C.ALERT_COUNT + 1
    ALERT_NUMBER = C.ALERT_COUNT
    message = update.message.text
    message = message.split(" ")
    token = str(message[0]+"inr").lower()
    print_line()
    print(f"Alert Number: {ALERT_NUMBER}", file=open(C.LOG_FILE, 'a+'))
    print(f"Alert Plus(Invoked): {get_time()}", file=open(
        C.LOG_FILE, 'a+'))
    print(f"Executed By: {get_username(update, context)}", file=open(
        C.LOG_FILE, 'a+'))
    print(f"Text: {message}", file=open(C.LOG_FILE, 'a+'))
    if C.ALERT_COUNT > 6:
        update.message.reply_text(C.OOPS_NOT_POSSIBLE)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(get_rate()[token]['last'])
    except ValueError:
        print("Remarks: Value Error\n", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except TypeError:
        message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER} Terminated.\n"
        print(message, file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(message)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except:
        print("Remarks: NOT A TOKEN\n", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.OOPS_404)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    print("", file=open(C.LOG_FILE, 'a+'))
    expected_rate = round(current_rate + (current_rate/100*percentage), 2)
    message_set = Template(C.ALERT_PLUS_SET).substitute(ano=ALERT_NUMBER, token=token[:-3].upper(
    ), lprice=current_rate, aprice=expected_rate, percentage=percentage)
    update.message.reply_text(message_set, parse_mode=ParseMode.MARKDOWN)
    while True:
        try:
            current_rate = float(get_rate()[token]['last'])
        except TypeError:
            message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER} Terminated."
            print_line()
            print(message, file=open(C.LOG_FILE, 'a+'))
            update.message.reply_text(message)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            return -1
        if current_rate >= expected_rate:
            message_executed = Template(C.ALERT_PLUS_EXECUTED).substitute(
                ano=ALERT_NUMBER, token=token.upper()[:-3], lprice=current_rate, percentage=percentage)
            update.message.reply_text(
                message_executed, parse_mode=ParseMode.MARKDOWN)
            print_line()
            print(f"Alert Number: {ALERT_NUMBER}", file=open(C.LOG_FILE, 'a+'))
            print(f"Alert Plus(Executed): {get_time()}\n", file=open(
                C.LOG_FILE, 'a+'))
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            break
        sleep(10)
    return 0


def alert_minus(update: Update, context: CallbackContext) -> int:
    """Alert when Token decreases by ceratin percentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    C.ALERT_COUNT = C.ALERT_COUNT + 1
    ALERT_NUMBER = C.ALERT_COUNT
    message = update.message.text
    message = message.split(" ")
    token = str(message[0]+"inr").lower()
    print_line()
    print(f"Alert Number: {ALERT_NUMBER}", file=open(C.LOG_FILE, 'a+'))
    print(f"Alert Minus(Invoked): {get_time()}", file=open(
        C.LOG_FILE, 'a+'))
    print(f"Executed By: {get_username(update, context)}", file=open(
        C.LOG_FILE, 'a+'))
    print(f"Text: {message}", file=open(C.LOG_FILE, 'a+'))
    if C.ALERT_COUNT > 6:
        update.message.reply_text(
            C.OOPS_NOT_POSSIBLE, file=open(C.LOG_FILE, 'a+'))
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(get_rate()[token]['last'])
    except ValueError:
        print("Remarks: Value Error\n", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except TypeError:
        message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER} Terminated.\n"
        print(message, file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(message)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except:
        print("Remarks: NOT A TOKEN\n", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.OOPS_404)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    print("", file=open(C.LOG_FILE, 'a+'))
    expected_rate = round(current_rate - (current_rate/100*percentage), 2)
    message_set = Template(C.ALERT_MINUS_SET).substitute(ano=ALERT_NUMBER, token=token[:-3].upper(
    ), lprice=current_rate, aprice=expected_rate, percentage=percentage)
    update.message.reply_text(message_set, parse_mode=ParseMode.MARKDOWN)
    while True:
        try:
            current_rate = float(get_rate()[token]['last'])
        except TypeError:
            message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER} Terminated."
            print_line()
            print(message, file=open(C.LOG_FILE, 'a+'))
            update.message.reply_text(message)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            return -1
        if current_rate <= expected_rate:
            message_executed = Template(C.ALERT_MINUS_EXECUTED).substitute(
                ano=ALERT_NUMBER, token=token.upper()[:-3], lprice=current_rate, percentage=percentage)
            update.message.reply_text(
                message_executed, parse_mode=ParseMode.MARKDOWN)
            print_line()
            print(f"Alert Number: {ALERT_NUMBER}", file=open(C.LOG_FILE, 'a+'))
            print(f"Alert Minus(Executed): {get_time()}\n", file=open(
                C.LOG_FILE, 'a+'))
            C.ALERT_COUNT = C.ALERT_COUNT - 1
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
    if token is None:
        token = update.message.text[:-4].lower()
    tokeninr = token + "inr"
    tokenusd = token + "usdt"
    print_line()
    print(f"Command: {token}rate", file=open(C.LOG_FILE, 'a+'))
    print(f"Time: {get_time()}", file=open(C.LOG_FILE, 'a+'))
    print(f"Token: {token.upper()}", file=open(C.LOG_FILE, 'a+'))
    print(f"User: {get_username(update, context)}",
          file=open(C.LOG_FILE, 'a+'))
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
        print("Remarks: NOT A TOKEN\n", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.OOPS_404)
        return -1
    print("", file=open(C.LOG_FILE, 'a+'))
    rate_text = Template(C.RATE_TEXT_INR).substitute(
        token=token.upper(), rate=nratei, lrate=lratei, hrate=hratei, vol=volumei, time=timei)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
    rate_text = Template(C.RATE_TEXT_USD).substitute(
        token=token.upper(), rate=nrateu, lrate=lrateu, hrate=hrateu, vol=volumeu, time=timeu)
    update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
    return 0


def all_rate(update: Update, context: CallbackContext) -> int:
    try:
        rate = get_rate()
    except:
        update.message.reply_text(C.OOPS_404)
        return -1
    print_line()
    print("Command: All Rates", file=open(C.LOG_FILE, 'a+'))
    print(f"Time: {get_time()}", file=open(C.LOG_FILE, 'a+'))
    print(f"User: {get_username(update, context)}\n",
          file=open(C.LOG_FILE, 'a+'))
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
    return 0
