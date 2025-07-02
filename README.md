Hi, this is my first project, but I'm sure few people are interested in that, so I'll leave detailed instructions for those who are seeing code for the first time, and how to set up the bot:

1 - First, you need to download the pip package installer (you can Google it and see how)
2 - Next, in the code editor, in the terminal (ctrl + Shift + (\` or ~), type `pip install pyTelegramBotAPI` 
The installation should start and several lines should appear in the terminal.
3 - Go to the const.py file and change the lines (`FILE_PATH` = path to the data_pssword.json file), (`TOKEN` = according to the instructions in the file), (`ADMIN_CHAT_ID` = I'll explain below how to get this id)
3.5 - ADMIN_CHAT_ID - find line 268 in password_bot.py and add a # sign in front of it, and in the send_welcome function - find it in the search (ctrl + f) and type the line `print(message.chat.id)` at the end
4 - Run the file, and press start in the dialog with the bot

Good luck !
