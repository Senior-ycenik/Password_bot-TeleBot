from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#  обычные переменные для работы (Поменяйте названия если это необходимо)
FILE_PATH = r"C:\TelegramBot_with_TeleBot\data_passwords.json"

#  токен вашего бота (от @BotFather)
TOKEN = "YOU_TOKEN"

# exm : "1234567890:xXxxXx-XxXx-xxxXXX012xxxXXxX45Xx_XX"
ADMIN_CHAT_ID = """YOUR_INT_CHAT_ID"""
   #  example : 1234567890 - Можно получить в meessage.chat.id:

#  тексты ошибок и приветствия (константы)
NO, YES = '❌', '✅'

R, F = "🗑️", "🔍"

TEXT_ERROR = "The fields for name and password are mandatory, please try again"

DONT_HAVE_PASSWORD = NO + "You could not find a password, but you can add such an Add ➕ function"

FIRST_GREETING = """Hi there! 😊
I'm your personal assistant, here to help with convenient storage
and password recording 🔐
/start - Restarting the bot 🔄
/help - Displays all available commands"""

GREETING = """Hi there! 😊
I'm your personal assistant, here to help with convenient storage
and password recording 🔐
/start - Restarting the bot 🔄

Here's the list of commands:
Add ➕   ⟹  Add a password to your collection
|- name (you will look for it)
|- password or random (12 characters)
|- description (optional)
Passwords 📂   ⟹  Your saved passwords
Search 🔍:
|- Remove 🗑️  ⟹  delete site by name
All clear ⚠️  ⟹  Deletes list of dictionaries"""

COMMAND_LIST = [
   types.BotCommand("start", "Start the bot"),
   types.BotCommand("help", "Display available commands")]

ADMIN_COMMAND_LIST = [
   types.BotCommand("start", "Start the bot"),
   types.BotCommand("help", "Display available commands"),
   types.BotCommand("stop", "Turn off the bot")]

COMMAND_ENABLE = [types.BotCommand("enable", "Turn on the bot")]

FIND_KEYBOARD = InlineKeyboardMarkup()
FIND_KEYBOARD.add(InlineKeyboardButton(text="Search 🔍", switch_inline_query_current_chat=''))