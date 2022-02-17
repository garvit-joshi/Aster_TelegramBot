# Aster_TelegramBot
Aster - A Telegram Bot for WazirX Crypto Exachange Analysis

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/garvit-joshi/Aster_TelegramBot)


## :zap: Installation
**1. Clone this repo by running either of the below commands.**

    https : `git clone https://github.com/garvit-joshi/Aster_TelegramBot.git`
  
    ssh : `git@github.com:garvit-joshi/Aster_TelegramBot.git`

**2. Now, run the following commands:**

```bash
cd Aster_TelegramBot
pip install -r requirements.txt
```
This will install all the project dependencies.

Note: Recommended way is to first create a virtual environment and then install the dependencies.

**3. Configure Bot Key:**

**File: secrets.ini**
```bash
echo "[KEYS]\nAPI_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" > secrets.ini
```
A file ```secrets.ini``` is missing as it contains a token to access the HTTP API of [Aster](t.me/Aster_Robot). The file is structured in this way: 
```
[KEYS]
API_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

**4. :tada: Run the bot:**
```bash
python3 main.py
```

## :page_facing_up: License
[MIT](./LICENSE) © [Garvit Joshi](https://github.com/garvit-joshi)
