import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to start the bot and greet users
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a link to a website to extract faculty information.')

# Function to extract faculty information from a given URL
def extract_info(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()  # Get the URL from the user's message
    
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
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
    
    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"An error occurred with the request to the URL: {e}")
        logger.error(f"Request to URL {url} failed: {e}")
    
    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")
        logger.error(f"Error occurred while processing URL {url}: {e}")

# Function to handle any other messages that are not commands
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("I'm sorry, I don't understand that command. Please use /start to begin.")

def main() -> None:
    # Initialize the bot with the token from environment variable
    TOKEN = os.getenv('7363675665:AAG8SE-Xr5WtLD3Vvs54kkHDGGrXalakOR8')
    if not TOKEN:
        logger.error('Telegram bot token not found. Set the TELEGRAM_BOT_TOKEN environment variable.')
        return
    
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("extract", extract_info))
    
    # Add message handler for non-command messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    # Start the Bot
    updater.start_polling()
    logger.info("Bot started. Press Ctrl+C to stop.")
    
    # Run the bot until Ctrl+C is pressed
    updater.idle()

if __name__ == '__main__':
    main()
