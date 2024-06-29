import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define the command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a link to a website to extract faculty information.')

def extract_info(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract faculty information (customize this part based on the website's structure)
        faculty_info = ""
        for faculty in soup.select('.faculty-class'):  # Update the CSS selector as needed
            faculty_info += faculty.get_text(separator="\n") + "\n\n"

        if faculty_info:
            update.message.reply_text(f"Faculty Information:\n\n{faculty_info}")
        else:
            update.message.reply_text("No faculty information found.")

    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

def main() -> None:
    # Initialize the bot with the token
    updater = Updater('7362981420:AAHkxLiFnAIys890b-WXwH23CsQcb-7OaBI')

    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("extract", extract_info))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
