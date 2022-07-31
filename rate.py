from datetime import datetime
from string import Template
from time import sleep

import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

import constants as C

wazirx_response = 0


def get_time(update: Update = None):
    """Gets Current Time

    Returns:
        HH:MM:SS {AM/PM} DD/MM/YYYY
    """
    if update is None:
        return datetime.now().strftime(C.TIME_FORMAT)
    return update.message.date.astimezone().strftime(C.TIME_FORMAT)


def get_username(update: Update, context: CallbackContext):
    """Gets Username of a person

    Returns:
        username
    """
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the person
    username = context.bot.getChatMember(chat_id, user_id).user.username
    if username is None:
        username = context.bot.getChatMember(chat_id, user_id).user.full_name
        username = username + "(Name)"
    return username


def print_logs(log_message):
    """Writes logs in logs.txt"""
    line = "-------------\n"
    log_message = line + log_message + line
    with open(C.LOG_FILE, "a+", encoding="utf8") as log_file:
        print(log_message, file=log_file)


def get_rate():
    """GET request to WazirX api

    Updates Global Variable: wazirx_response

    Returns:
        -1: If API cannot be fetched successfully
         0: If API was Successfully fetched
    """
    global wazirx_response
    try:
        wazirx_request = requests.get("https://api.wazirx.com/api/v2/tickers")
    except:
        log_text = "API Cannot be fetched\n"
        log_text = log_text + f"Time: {get_time()}\n"
        print_logs(log_text)
        sleep(20)
        return -1
    if wazirx_request.status_code != 200:
        log_text = f"Status Code: {wazirx_request.status_code}\n"
        log_text = log_text + str(wazirx_request.headers) + "\n"
        log_text = log_text + f"Time: {get_time()}\n"
        print_logs(log_text)
        if wazirx_request.status_code in range(400, 500):
            sleep(600)
        else:
            sleep(30)
        return -1
    wazirx_response = wazirx_request.json()
    return 0


def cancel_alert(update: Update, context: CallbackContext) -> int:
    """Cancels the alerts

    Returns:
        -1: If Not called by Developer, already a thread running
         0: All Alerts are cancelled
    """
    log_text = f"Command: Cancel Alerts\nUser: {get_username(update, context)}\n"
    log_text = log_text + f"Invocation Time: {get_time(update)}\n"
    if get_username(update, context) != "garvit_joshi9":
        log_text = log_text + "Remarks: Not a Developer\n"
        print_logs(log_text)
        update.message.reply_text(C.ERROR_PRIVILEGE)
        return -1
    if C.CANCEL_ALERT_FLAG == 1:
        log_text = log_text + "Remarks: Already a thread running\n"
        print_logs(log_text)
        return -1
    C.CANCEL_ALERT_FLAG = 1
    message = "Alerts will be terminated withing 10 sec."
    update.message.reply_text(message)
    sleep(10)  # Sleep until All alerts are terminated.
    C.CANCEL_ALERT_FLAG = 0
    C.ALERT_NUMBER = 0
    C.ALERT_COUNT = 0
    C.WAZIRX_API_THRESHOLD = 15
    log_text = log_text + f"Sent Time: {get_time()}\n"
    update.message.reply_text("All Alerts Cancelled!!")
    print_logs(log_text)
    return 0


def rate_command(update: Update, context: CallbackContext, token=None) -> int:
    """Reply with real time Token rate

    Keyword arguments:
        update: This object represents an incoming update.
        context: This is a context object error handler.
    """
    command = update.message.text
    log_text = f"Command: {command}\n"
    if command[0] == "/":
        command = command[1:]
    if token is None:
        token = command[:-4].lower()
    tokeninr = token + "inr"
    tokenusd = token + "usdt"
    log_text = log_text + f"Invocation Time: {get_time(update)}\n"
    log_text = log_text + f"Token: {token.upper()}\n"
    log_text = log_text + f"User: {get_username(update, context)}\n"
    token_flag = 0
    rate = wazirx_response
    if rate == -1:
        update.message.reply_text(C.OOPS_404)
        return -1
    try:
        nratei = rate[tokeninr]["last"]
        lratei = rate[tokeninr]["low"]
        hratei = rate[tokeninr]["high"]
        volumei = rate[tokeninr]["volume"]
        timei = datetime.fromtimestamp(rate[tokeninr]["at"]).strftime(C.TIME_FORMAT)
        rate_text = Template(C.RATE_TEXT_INR).substitute(
            token=token.upper(),
            rate=nratei,
            lrate=lratei,
            hrate=hratei,
            vol=volumei,
            time=timei,
        )
        log_text = log_text + f"Sent Time: {get_time()}\n"
        update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
    except:
        token_flag = 1
    try:
        nrateu = rate[tokenusd]["last"]
        lrateu = rate[tokenusd]["low"]
        hrateu = rate[tokenusd]["high"]
        volumeu = rate[tokenusd]["volume"]
        timeu = datetime.fromtimestamp(rate[tokenusd]["at"]).strftime(C.TIME_FORMAT)
        rate_text = Template(C.RATE_TEXT_USD).substitute(
            token=token.upper(),
            rate=nrateu,
            lrate=lrateu,
            hrate=hrateu,
            vol=volumeu,
            time=timeu,
        )
        update.message.reply_text(rate_text, parse_mode=ParseMode.MARKDOWN)
    except:
        if token_flag == 1:
            log_text = log_text + "Remarks: NOT A TOKEN\n"
            print_logs(log_text)
            update.message.reply_text(C.OOPS_404)
            return -1
    print_logs(log_text)
    return 0


def all_rate(update: Update, context: CallbackContext) -> int:
    """Replies with some famous token rates

    Keyword arguments:
        update: This object represents an incoming update.
        context: This is a context object error handler.
    """
    try:
        rate = wazirx_response
    except:
        update.message.reply_text(C.OOPS_404)
        return -1
    log_text = "Command: All Rates\n"
    log_text = log_text + f"Invocation Time: {get_time(update)}\n"
    log_text = log_text + f"User: {get_username(update, context)}\n"
    message = ""
    for token in C.inrtokens:
        tokeninr = token + "inr"
        token_rate = rate[tokeninr]["last"]
        message = message + token.upper() + ": " + token_rate + " INR\n"
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    message = ""
    for token in C.usdttokens:
        tokenusdt = token + "usdt"
        token_rate = rate[tokenusdt]["last"]
        message = message + token.upper() + ": " + token_rate + " USDT\n"
    log_text = log_text + f"Sent Time: {get_time()}\n"
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    print_logs(log_text)
    return 0


def alert_plus(update: Update, context: CallbackContext) -> int:
    """Alert when Token increases by ceratin persentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    C.WAZIRX_API_THRESHOLD = 3
    C.ALERT_COUNT = C.ALERT_COUNT + 1
    C.ALERT_NUMBER = C.ALERT_NUMBER + 1
    ALERT_NUMBER_ = C.ALERT_NUMBER
    message = update.message.text
    message = message.split(" ")
    token = str(message[0] + "inr").lower()
    log_text = f"Alert Number: {ALERT_NUMBER_}\n"
    log_text = log_text + f"Alert Plus(Invoked): {get_time(update)}\n"
    log_text = log_text + f"User: {get_username(update, context)}\n"
    log_text = log_text + f"Text: {message}\n"
    if C.ALERT_COUNT > C.WORKERS - 4:
        update.message.reply_text(C.OOPS_NOT_POSSIBLE)
        log_text = log_text + "Remarks: No More alerts possible\n"
        print_logs(log_text)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(wazirx_response[token]["last"])
    except ValueError:
        log_text = log_text + "Remarks: Value Error\n"
        print_logs(log_text)
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except TypeError:
        message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER_} Terminated.\n"
        log_text = log_text + message
        print_logs(log_text)
        update.message.reply_text(message)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except:
        log_text = log_text + "Remarks: NOT A TOKEN\n"
        print_logs(log_text)
        update.message.reply_text(C.OOPS_404)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    expected_rate = round(current_rate + (current_rate / 100 * percentage), 2)
    message_set = Template(C.ALERT_PLUS_SET).substitute(
        ano=ALERT_NUMBER_,
        token=token[:-3].upper(),
        lprice=current_rate,
        aprice=expected_rate,
        percentage=percentage,
    )
    update.message.reply_text(message_set, parse_mode=ParseMode.MARKDOWN)
    log_text = log_text + f"Sent Time: {get_time()}\n"
    print_logs(log_text)
    while True:
        if C.CANCEL_ALERT_FLAG == 1:
            message = f"Alert Number: {ALERT_NUMBER_} Cancelled\n"
            update.message.reply_text(message)
            message = message + f"User: {get_username(update, context)}\n"
            print_logs(message)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            return 0
        try:
            current_rate = float(wazirx_response[token]["last"])
        except TypeError:
            log_text = f"Alert Number:{ALERT_NUMBER_}\nWazirX not responding!!\n"
            print_logs(log_text)
        if current_rate >= expected_rate:
            message_executed = Template(C.ALERT_PLUS_EXECUTED).substitute(
                ano=ALERT_NUMBER_,
                token=token.upper()[:-3],
                lprice=current_rate,
                percentage=percentage,
            )
            update.message.reply_text(message_executed, parse_mode=ParseMode.MARKDOWN)
            log_text = f"Alert Number: {ALERT_NUMBER_}\n"
            log_text = log_text + f"Alert Plus(Executed): {get_time()}\n"
            print_logs(log_text)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            break
        sleep(6)
    return 0


def alert_plus_minus(update: Update, context: CallbackContext) -> int:
    """
    Alert when Token increases/decreases by ceratin percentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    C.WAZIRX_API_THRESHOLD = 3
    C.ALERT_COUNT = C.ALERT_COUNT + 1
    C.ALERT_NUMBER = C.ALERT_NUMBER + 1
    ALERT_NUMBER_ = C.ALERT_NUMBER
    message = update.message.text
    message = message.split(" ")
    token = str(message[0] + "inr").lower()
    log_text = f"Alert Number: {ALERT_NUMBER_}\n"
    log_text = log_text + f"Alert Plus-Minus(Invoked): {get_time(update)}\n"
    log_text = log_text + f"User: {get_username(update, context)}\n"
    log_text = log_text + f"Text: {message}\n"
    if C.ALERT_COUNT > C.WORKERS - 4:
        update.message.reply_text(C.OOPS_NOT_POSSIBLE)
        log_text = log_text + "Remarks: No More alerts possible\n"
        print_logs(log_text)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(wazirx_response[token]["last"])
    except ValueError:
        log_text = log_text + "Remarks: Value Error\n"
        print_logs(log_text)
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except TypeError:
        message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER_} Terminated.\n"
        log_text = log_text + message
        update.message.reply_text(message)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except:
        log_text = log_text + "Remarks: NOT A TOKEN\n"
        print_logs(log_text)
        update.message.reply_text(C.OOPS_404)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    expected_rate_plus = round(current_rate + (current_rate / 100 * percentage), 2)
    expected_rate_minus = round(current_rate - (current_rate / 100 * percentage), 2)
    message_set_plus = Template(C.ALERT_PLUS_SET).substitute(
        ano=ALERT_NUMBER_,
        token=token[:-3].upper(),
        lprice=current_rate,
        aprice=expected_rate_plus,
        percentage=percentage,
    )
    message_set_minus = Template(C.ALERT_MINUS_SET).substitute(
        ano=ALERT_NUMBER_,
        token=token[:-3].upper(),
        lprice=current_rate,
        aprice=expected_rate_minus,
        percentage=percentage,
    )
    log_text = log_text + f"Sent Time: {get_time()}\n"
    update.message.reply_text(message_set_plus, parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(message_set_minus, parse_mode=ParseMode.MARKDOWN)
    print_logs(log_text)
    while True:
        if C.CANCEL_ALERT_FLAG == 1:
            message = f"Alert Number: {ALERT_NUMBER_} Cancelled\n"
            update.message.reply_text(message)
            message = message + f"User: {get_username(update, context)}\n"
            print_logs(message)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            return 0
        try:
            current_rate = float(wazirx_response[token]["last"])
        except TypeError:
            log_text = f"Alert Number:{ALERT_NUMBER_}\nWazirX not responding!!\n"
            print_logs(log_text)
        if current_rate >= expected_rate_plus:
            message_executed = Template(C.ALERT_PLUS_EXECUTED).substitute(
                ano=ALERT_NUMBER_,
                token=token.upper()[:-3],
                lprice=current_rate,
                percentage=percentage,
            )
            update.message.reply_text(message_executed, parse_mode=ParseMode.MARKDOWN)
            log_text = f"Alert Number: {ALERT_NUMBER_}\n"
            log_text = log_text + f"Alert Plus-Minus(Executed: PLUS): {get_time()}\n"
            print_logs(log_text)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            break
        if current_rate <= expected_rate_minus:
            message_executed = Template(C.ALERT_MINUS_EXECUTED).substitute(
                ano=ALERT_NUMBER_,
                token=token.upper()[:-3],
                lprice=current_rate,
                percentage=percentage,
            )
            update.message.reply_text(message_executed, parse_mode=ParseMode.MARKDOWN)
            log_text = f"Alert Number: {ALERT_NUMBER_}\n"
            log_text = log_text + f"Alert Plus-Minus(Executed: MINUS): {get_time()}\n"
            print_logs(log_text)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            break
        sleep(6)
    return 0


def alert_minus(update: Update, context: CallbackContext) -> int:
    """Alert when Token decreases by ceratin percentage

    Returns:
        -1: If Exceptions occours
        0:  Alert Executes
    """
    C.WAZIRX_API_THRESHOLD = 3
    C.ALERT_COUNT = C.ALERT_COUNT + 1
    C.ALERT_NUMBER = C.ALERT_NUMBER + 1
    ALERT_NUMBER_ = C.ALERT_NUMBER
    message = update.message.text
    message = message.split(" ")
    token = str(message[0] + "inr").lower()
    log_text = f"Alert Number: {ALERT_NUMBER_}\n"
    log_text = log_text + f"Alert Minus(Invoked): {get_time(update)}\n"
    log_text = log_text + f"User: {get_username(update, context)}\n"
    log_text = log_text + f"Text: {message}\n"
    if C.ALERT_COUNT > C.WORKERS - 4:
        update.message.reply_text(C.OOPS_NOT_POSSIBLE, file=open(C.LOG_FILE, "a+"))
        log_text = log_text + "Remarks: No More alerts possible\n"
        print_logs(log_text)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    try:
        percentage = float(message[1])
        if percentage <= 0:
            raise ValueError
        current_rate = float(wazirx_response[token]["last"])
    except ValueError:
        log_text = log_text + "Remarks: Value Error\n"
        print_logs(log_text)
        update.message.reply_text(C.OOPS_WRONG_FORMAT)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except TypeError:
        message = f"WazirX not responding!!\nAlert Number:{ALERT_NUMBER_} Terminated.\n"
        log_text = log_text + message
        print_logs(log_text)
        update.message.reply_text(message)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    except:
        log_text = log_text + "Remarks: NOT A TOKEN\n"
        print_logs(log_text)
        update.message.reply_text(C.OOPS_404)
        C.ALERT_COUNT = C.ALERT_COUNT - 1
        return -1
    expected_rate = round(current_rate - (current_rate / 100 * percentage), 2)
    message_set = Template(C.ALERT_MINUS_SET).substitute(
        ano=ALERT_NUMBER_,
        token=token[:-3].upper(),
        lprice=current_rate,
        aprice=expected_rate,
        percentage=percentage,
    )
    log_text = log_text + f"Sent Time: {get_time()}\n"
    update.message.reply_text(message_set, parse_mode=ParseMode.MARKDOWN)
    print_logs(log_text)
    while True:
        if C.CANCEL_ALERT_FLAG == 1:
            message = f"Alert Number: {ALERT_NUMBER_} Cancelled\n"
            update.message.reply_text(message)
            message = message + f"User: {get_username(update, context)}\n"
            print_logs(message)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            return 0
        try:
            current_rate = float(wazirx_response[token]["last"])
        except TypeError:
            log_text = f"Alert Number:{ALERT_NUMBER_}\nWazirX not responding!!\n"
            print_logs(log_text)
        if current_rate <= expected_rate:
            message_executed = Template(C.ALERT_MINUS_EXECUTED).substitute(
                ano=ALERT_NUMBER_,
                token=token.upper()[:-3],
                lprice=current_rate,
                percentage=percentage,
            )
            update.message.reply_text(message_executed, parse_mode=ParseMode.MARKDOWN)
            log_text = f"Alert Number: {ALERT_NUMBER_}\n"
            log_text = log_text + f"Alert Minus(Executed): {get_time()}\n"
            print_logs(log_text)
            C.ALERT_COUNT = C.ALERT_COUNT - 1
            break
        sleep(6)
    return 0
