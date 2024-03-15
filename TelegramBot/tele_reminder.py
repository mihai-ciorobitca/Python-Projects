from telegram import Bot
import asyncio
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve values from environment variables
CHAT_ID = getenv("ID")
TOKEN = getenv("TOKEN")

# Function to send a reminder message
async def send_message():
    # Create a Telegram Bot instance
    bot = Bot(token=TOKEN)

    try:
        # Send a reminder message to the specified chat ID
        _ = await bot.send_message(
            chat_id=CHAT_ID,
            text="⏰ Time to drink some water! 💧"
        )

        # Print a success message along with the timestamp
        now = datetime.now()
        print(f"✅ Message sent successfully at {now}")
    except Exception as e:
        # Handle any errors that may occur during message sending
        print(f"❌ Error: {e}")

# Main entry point of the script
if __name__ == "__main__":
    # Run the send_message function using asyncio
    asyncio.run(send_message())