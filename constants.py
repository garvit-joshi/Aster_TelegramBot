LOG_FILE = "Main.log"  # Log File

WORKERS = 25

WAZIRX_API_THRESHOLD = 15  # Seconds PAUSE AFTER EVERY API CALL

ALERT_COUNT = 0  # No. of Alerts Running

ALERT_NUMBER = 0  # Unique Alert Number

CANCEL_ALERT_FLAG = 0

ERROR_PRIVILEGE = "Sorry!! This command can only be executed by a developer"

RATE_TEXT_INR = """
***Token Rate $token/INR***
***Rate:*** $rate INR
***Low:*** $lrate INR
***High:*** $hrate INR
***Volume:*** $vol
***Time:*** $time
"""

ALERT_PLUS_SET = """
***Alert $token***
***Alert Number: $ano***
Latest $token price: $lprice INR
Alert when $token >= $aprice INR
Percentage Increase: $percentage%
"""

ALERT_PLUS_EXECUTED = """
***Alert Executed***
***Alert Number: $ano***
Latest $token price: $lprice INR
Percentage Increased: $percentage%
"""

ALERT_MINUS_SET = """
***Alert $token***
***Alert Number: $ano***
Latest $token price: $lprice INR
Alert when $token <= $aprice INR
Percentage Decrease: $percentage%
"""

ALERT_MINUS_EXECUTED = """
***Alert Executed***
***Alert Number: $ano***
Latest $token price: $lprice INR
Percentage Decreased: $percentage%
"""

RATE_TEXT_USD = """
***Token Rate $token/USDT***
***Rate:*** $rate USDT
***Low:*** $lrate USDT
***High:*** $hrate USDT
***Volume:*** $vol
***Time:*** $time
"""

OOPS_404 = """
404! Your token ain't here kid...
"""

OOPS_NOT_POSSIBLE = f"Oops! Only {WORKERS-4} concurrent alerts possible kid..."

OOPS_WRONG_FORMAT = """
Not sure what you are talking about... \U0001F928	
"""

HELP_TEXT = """
Hey There!
My name is Aster. Aster comes from the ancient Greek word ἀστήρ (astḗr), meaning "star".\n
Currently, I am in Development. Some commands that I support:
1. /start\n
2. /help\n
3. /source\n
4. /all\_rates\n
5. Type Coin Name with RATE at last. eg, btcrate\n
6. Alert eg, (btc 8 -): Alert when BTC rate Decreases by 8%.\n
7. Alert eg, (matic 8 +): Alert when MATIC rate increases by 8%.\n
8. Alert eg, (eth 8 +-): Alert when ETH rate increases or decreases by 8%.\n\n 
As I am an Open Source Project, You can contribute to my development.\n
Link: [here](https://github.com/garvit-joshi/Aster_TelegramBot)
I am learning new things everyday. \U0001F60E
"""

SOURCE = """
Hey there $name,
You can find my Source code [here](https://github.com/garvit-joshi/Aster_TelegramBot).
In case of bottlenecks please feel free to message [@garvit_joshi9](t.me/garvit_joshi9).
Happy Coding !! \U0001F60E
"""

inrtokens = [
    "btc",
    "matic",
    "eth",
    "hbar",
    "dock",
    "doge",
    "xrp",
    "ada",
    "xlm",
    "link",
    "trx",
]
usdttokens = [
    "btc",
    "matic",
    "eth",
    "hbar",
    "doge",
    "xrp",
    "ada",
    "xlm",
    "link",
    "trx",
    "xmr",
    "theta",
    "tfuel",
]
