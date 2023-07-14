# Author : Soubhagyajit Borah
# More about this project : www.sjbtechcenter.online

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import openai

bot_token = 'YOUR TOKEN '
openai_api_key = 'YOUR KEY'

with open("chat.txt", "r") as f:
    chat = f.read()

bot = telegram.Bot(token=bot_token)
openai.api_key = openai_api_key

def help_command(update, context):
    chat_id = update.message.chat_id

    help_message = "Commands:\n /name\n /desc\n /website\n /contact"
    bot.send_message(chat_id=chat_id, text=help_message)

def name_command(update, context):
    chat_id = update.message.chat_id

    name_message = "Bot Name: Soubhagyajit"
    bot.send_message(chat_id=chat_id, text=name_message)

def desc_command(update, context):
    chat_id = update.message.chat_id

    desc_message = "Bot Name: Soubhagyajit\nA chat bot created by Soubhagyajit Borah. Using OpenAI API for conversation and chatting."
    bot.send_message(chat_id=chat_id, text=desc_message)

def website_command(update, context):
    chat_id = update.message.chat_id

    website_message = "Website: https://sjbtechcenter.online"
    bot.send_message(chat_id=chat_id, text=website_message)

def contact_command(update, context):
    chat_id = update.message.chat_id

    contact_message = "Contact us at soubhagyajitborah@gmail.com"
    bot.send_message(chat_id=chat_id, text=contact_message)

def start_command(update, context):
    chat_id = update.message.chat_id
    user = update.message.from_user
    first_name = user.first_name

    welcome_message = f"Welcome, {first_name}! Thank you for chatting with me."
    bot.send_message(chat_id=chat_id, text=welcome_message)

def handle_message(update, context):
    message = update.message.text
    chat_id = update.message.chat_id
    user = update.message.from_user
    first_name = user.first_name

    global chat
    chat += message

    if update.message.chat.type == 'private':
        # Process the message for individual chat
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{chat}\n Soubhagyajit:",
            temperature=1,
            max_tokens=2560,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        message_to_send = response.choices[0].text

        print("\n",update.message.chat.type, chat_id, " : ", first_name, " : ", message, "\n")

        if chat_id != bot.get_me().id:
            bot.send_message(chat_id=chat_id, text=message_to_send)
            print("Respond: ", message_to_send)
    elif update.message.chat.type == 'group':
        # Check if the bot is mentioned in the message
        if bot.username.lower() in message.lower():
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=chat,
                temperature=1,
                max_tokens=2560,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            message_to_send = response.choices[0].text

            print("\n",update.message.chat.type, chat_id, " : ", first_name, " : ", message, "\n")

            if chat_id != bot.get_me().id:
                bot.send_message(chat_id=chat_id, text=message_to_send)
                print("Respond: ", message_to_send)

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

help_handler = CommandHandler('help', help_command)
name_handler = CommandHandler('name', name_command)
desc_handler = CommandHandler('desc', desc_command)
website_handler = CommandHandler('website', website_command)
contact_handler = CommandHandler('contact', contact_command)
start_handler = CommandHandler('start', start_command)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(help_handler)
dispatcher.add_handler(name_handler)
dispatcher.add_handler(desc_handler)
dispatcher.add_handler(website_handler)
dispatcher.add_handler(contact_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
