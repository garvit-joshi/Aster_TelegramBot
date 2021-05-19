# Aster_TelegramBot
Aster - A Telegram Bot for WazirX Crypto Exachange Analysis

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

**3. Configure Missing Files:**

**File: secrets.py**
```bash
echo "API_KEY = 'YOUR_BOT_API_KEY'" > secrets.py
```
A file ```secrets.py``` is missing as it contains a token to access the HTTP API of [Aster](t.me/Aster_Robot). The file is structured in this way: 
```python
API_KEY = 'YOUR_BOT_API_KEY'
```

**4. :tada: Run the bot:**
```bash
python3 main.py
```

## :page_facing_up: License
[MIT](./LICENSE) © [Garvit Joshi](https://github.com/garvit-joshi)
