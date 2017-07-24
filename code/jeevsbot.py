import telepot
from pprint import pprint
import requests
import os

bot_token = os.environ["BOT_TOKEN"]


bot = telepot.Bot(bot_token)
bot.getMe()
response = bot.getUpdates()
pprint(response)
