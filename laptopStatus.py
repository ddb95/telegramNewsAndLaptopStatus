#!/usr/bin/python3.6

import telegram
from config import telegram_token
import time

if __name__ == '__main__':
    timeWhenOpened = time.asctime(time.localtime(time.time()))
    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id="@laptopStatus", text="Laptop Started @ " + timeWhenOpened,
                     parse_mode=telegram.ParseMode.HTML)
