from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import string
import random
import json
from const import *
import time
from uuid import uuid4

bot = TeleBot(TOKEN)

BOT_WORK = True

#  чтение файла
try:
    with open(FILE_PATH, "r") as file_read:
        DATA = json.load(file_read)
except (FileNotFoundError, json.JSONDecodeError):
    DATA = {}

def Remove(*, callback: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Remove 🗑️", callback_data=callback))
    return keyboard

def Replace_symbol(*, string):
    if string is None:
        return ''

    reserved_chars = r'_*[]()~`>#+-=|{}.!'
    for char in reserved_chars:
        string = string.replace(char, '\\' + char)
    return string

#  Создание inline резльтатов
FIND_RESULT = [types.InlineQueryResultArticle(
            id=str(uuid4()), title='🔍  Find', description='The last 15 passwords 🗂\nEnter the name for the search 🔍 . . . ',
            thumbnail_url="https://symbl.cc/i/webp/f0/eaf0e45fea619f5e8e0466aae33cf0.webp",
            input_message_content=types.InputTextMessageContent(message_text='You need to choose a password in order to find it 🔍'),
            reply_markup=FIND_KEYBOARD), ""]
DONT_RESULT = [types.InlineQueryResultArticle(
            id=str(uuid4()), title="You don't have password" + NO, description=DONT_HAVE_PASSWORD[1:],
            thumbnail_url="https://symbl.cc/i/webp/59/55d3ed33dc4daf9ec21721bd1c561d.webp",
            input_message_content=types.InputTextMessageContent(message_text="➖➖➖➖➖\n" + DONT_HAVE_PASSWORD))]

RESULT = {}
for id in DATA:
    index = 1
    chat_id_data = [FIND_RESULT.copy()]
    for name, info in DATA[id].items():
        text = f"➖➖➖➖➖\n`{Replace_symbol(string=name)}`\n`{Replace_symbol(string=info["password"])}`" + f"\n➖➖➖➖➖\n_{Replace_symbol(string=info["description"])}_" * bool(info["description"])
        chat_id_data.append((types.InlineQueryResultArticle(
                        id=str(uuid4()),
                        title="➕" + name,
                        reply_markup=Remove(callback = str(index) + ' ' + name),
                        thumbnail_url="https://symbl.cc/i/webp/cf/74f1c87550d3e860f2b142917a42ba.webp",
                        input_message_content=types.InputTextMessageContent(message_text=text, parse_mode="MarkdownV2")), name))
        index += 1
    RESULT |= {int(id): chat_id_data}

#  Не реагировать на чат
FLAG_BOT = True
@bot.message_handler(func=lambda message: True and FLAG_BOT)
def cleanning(message) -> None:
    now_time = time.perf_counter()
    global old_time, FLAG_BOT
    if now_time - old_time > 2:
        FLAG_BOT = False
        for chat_id in DATA:
            bot.send_message(chat_id, FIRST_GREETING, reply_markup=markup)
        return

    old_time = time.perf_counter()

#  Создание кнопок
markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=False)
markup.row(*(KeyboardButton("Passwords 📂"), KeyboardButton("Add ➕")))
markup.row(*(KeyboardButton("Search 🔍"), KeyboardButton("All clear ⚠️")))

    #  Побочные функции
def set_description(*, mode: bool | None=True) -> True:  #  изменение описания бота
    description = FIRST_GREETING if mode else "I'am sorry, but bot is stopped 🔴"
    bot.set_my_description(description)

# изменение описания
set_description()

#  функция генерации случайного пароля
def random_password() -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(12))

# получение записей пользователя
def receive_a_message(message, *, name: str | None=None, password: str | None=None) -> TeleBot:
    if password:
        Add(name, password, message.text, int_chat_id=message.chat.id)
    elif name:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Skip ⏩"))
        bot.send_message(message.chat.id, "Enter a description (optional) ✍️", reply_markup=keyboard)
        return bot.register_next_step_handler(message, receive_a_message, name=name, password=message.text)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(f"Random 🎲"))
        bot.send_message(message.chat.id, "Enter a password or indicate: random your number 🔐", reply_markup=keyboard)
        return bot.register_next_step_handler(message, receive_a_message, name=message.text)

   #  Функции бота   
#  функция чтения всех паролей из файла
def Passwords(*, message) -> None:
    All_passwords = "You all passwords in the format:\nsite: password  📝\\(❌/✅\\) \\- discription" + "\n🔐  🔐  🔐\n"
    if not DATA.setdefault(str(message.chat.id), {}):
        bot.send_message(message.chat.id, DONT_HAVE_PASSWORD)
        return

    for name, value in DATA[str(message.chat.id)].items():
        password, disc = value.values()
        All_passwords += f"`{name}`  \\-\\>  `{password}`  📝" + (f'{YES}\n' if disc else f'{NO}\n')

    bot.send_message(message.chat.id, All_passwords, parse_mode="MarkdownV2")


#  Добавление пароля
def Add(*args, int_chat_id: int) -> None:
    str_chat_id = str(int_chat_id)
    name, password, description = args

    if description == f"Skip ⏩":
        description = None
    if password == f"Random 🎲":
        password = random_password()
    text = f"`{name}`  \\-\\>  `{password}`  saved to your passwords {YES}"

    if not DATA.setdefault(str_chat_id): #  если нет пользователя
        DATA[str_chat_id] = {name:{"password":password, "description":description}}
    elif not DATA[str_chat_id].setdefault(name): # если нет имени
        DATA[str_chat_id][name] = {"password":password, "description":description}
    else:  #  если имя уже существует
        for last_name in DATA[str_chat_id]:
            if name.lower() == last_name.lower():
                last_password = DATA[str_chat_id][last_name]["password"]
                break
        text = f"`{last_name}`  \\-  `{last_password}`\nchanged to the name\n`{name}`  \\-  `{password}` 🔄"
        DATA[str_chat_id][name] = {"password":password, "description":description}

    text_result = f"➖➖➖➖➖\n`{Replace_symbol(string=name)}`\n`{Replace_symbol(string=password)}`" + f"\n➖➖➖➖➖\n_{Replace_symbol(string=description)}_" * bool(description)
    RESULT.setdefault(int_chat_id, [FIND_RESULT.copy()])
    RESULT[int_chat_id].append((types.InlineQueryResultArticle(
                        id=str(uuid4()),
                        title="➕" + name,
                        reply_markup=Remove(callback = str(len(RESULT[int_chat_id])) + ' ' + name),
                        thumbnail_url="https://symbl.cc/i/webp/cf/74f1c87550d3e860f2b142917a42ba.webp",
                        input_message_content=types.InputTextMessageContent(message_text=text_result, parse_mode="MarkdownV2")), name))

    bot.send_message(int_chat_id, text, parse_mode="MarkdownV2", reply_markup=markup)

        
#  функция поиска пароля по названию сайта
def Search(*, chat_id) -> None:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Search in your passwords 🗂️", switch_inline_query_current_chat='')
    keyboard.add(button)

    bot.send_message(chat_id, 'To start searching for a password\nenter the name of the site', reply_markup=keyboard)


#  удаление всех паролей
def All_clear(*, message: TeleBot) -> None:
    int_chat_id = message.chat.id

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(NO, callback_data="not_clean"),
        InlineKeyboardButton(YES, callback_data="yes_clean"))

    bot.send_message(int_chat_id, "Are you sure you want to remove all the passwords?", reply_markup=keyboard)


#  обработчики сообщений тг
@bot.message_handler(commands=["start", "help", "stop"])
def send_welcome(message):
    text = message.text
    match text:
        case "/start":
            bot.reply_to(message, FIRST_GREETING, reply_markup=markup)
        case '/help':
            bot.reply_to(message, GREETING, reply_markup=markup)
        case '/stop':
            if message.chat.id == ADMIN_CHAT_ID:
                global BOT_WORK
                BOT_WORK = False
                bot.stop_polling()


#  обработчик для кнопок (и функции add) бота
@bot.message_handler(func=lambda message: True)
def process_the_button(message):
    int_chat_id = message.chat.id
    text = message.text
    match text:
        case "Passwords 📂":
            Passwords(message=message)
        case "Add ➕":
            bot.send_message(message.chat.id, "Enter a name or site 🗂")
            bot.register_next_step_handler(message, receive_a_message)
        case "Search 🔍":
            Search(chat_id=int_chat_id)
        case "All clear ⚠️":
            All_clear(message=message)
            

#  ответ на кнопки (под сообщениями)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    int_chat_id = call.from_user.id
    str_chat_id = str(int_chat_id)
    call_id = call.id
    call_data = call.data

    match call_data:
        case "yes_clean":
            if not DATA.setdefault(str_chat_id, {}):
                bot.send_message(int_chat_id, DONT_HAVE_PASSWORD)
                bot.answer_callback_query(call_id, DONT_HAVE_PASSWORD)
                return
            del DATA[str_chat_id]
            del RESULT[int_chat_id]
            
            bot.answer_callback_query(call_id, 'All your passwords are deleted' + R)
            bot.send_message(int_chat_id, 'All your passwords are deleted' + R)
            bot.edit_message_text(FIRST_GREETING, int_chat_id, call.message.message_id)

        case "not_clean":
            bot.answer_callback_query(call_id, 'Cansel' + NO)
            bot.edit_message_text(FIRST_GREETING, int_chat_id, call.message.message_id)

        case _:
            call_data = call_data.split(maxsplit=1)

            if DATA.get(str_chat_id):
                if DATA[str_chat_id].pop(call_data[1]):
                    del RESULT[int_chat_id][int(call_data[0])]
                    bot.answer_callback_query(call_id, "This password is deleted🗑️")
                    return

            bot.answer_callback_query(call_id, "It seems that you have already deleted the password")


# Обработчик inline запросов
@bot.inline_handler(func=lambda query: True)
def handle_inline_query(query):
    text = query.query
    chat_id = query.from_user.id

    if not DATA.get(str(chat_id)):
        bot.answer_inline_query(query.id, DONT_RESULT, cache_time=0)
    else:
        result, index = [], 0
        for answer in RESULT[chat_id]:
            if text.lower() in answer[1].lower() and index < 15:
                result.append(answer[0])
                index += 1

        bot.answer_inline_query(query.id, result, cache_time=0)


bot.set_my_commands(COMMAND_LIST)  #  добавление команд боту

bot.set_my_commands(ADMIN_COMMAND_LIST, scope=types.BotCommandScopeChat(ADMIN_CHAT_ID))

old_time = time.perf_counter()

print("Bot - start . . .")

while BOT_WORK:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}. \nPersonal after 40 seconds...")
        time.sleep(40)


set_description(mode=False)

#  Запись данных в файл (в случае остановки бота - эта функция не дает потерять все пароли)
with open(FILE_PATH, "w") as file_write:
    json.dump(DATA, file_write, indent=4)