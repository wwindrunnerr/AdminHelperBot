import telebot
import os
import sqlite3

from telebot import types 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, Application, MessageHandler, CommandHandler, filters, ContextTypes

load_dotenv()

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
name = None
#user_id = os.environ['USER_ID']


#ADMINPANEL
@bot.message_handler(commands=['start'])
def start(message:types.Message):

    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT auto_increment primary key, name VARCHAR(50), password VARCHAR(50))')
    connection.commit()
    cursor.close()
    connection.close()

    helpbtn = types.InlineKeyboardButton(text = 'Help', callback_data = 'help')
    privacybtn = types.InlineKeyboardButton(text = 'Privacy', callback_data='privacy')
    markup = types.InlineKeyboardMarkup([[helpbtn,privacybtn]])

    bot.send_message(message.chat.id, f'Heyo, let`s sigh up you first.\nPlease insert your login:')
    bot.register_next_step_handler(message, user_name)
    #bot.send_message(message.chat.id, f'Hi, {message.from_user.username}!\nWhat`s our next step?', reply_markup = markup)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f'Please insert your password:')
    bot.register_next_step_handler(message, user_password)

def user_password(message):
    password = hash(message.text.strip())

    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" % (name, password))
    connection.commit()
    cursor.close()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('User List', callback_data='userlist'))
    markup.add(types.InlineKeyboardButton('Clear User List', callback_data='clearlist'))
    bot.send_message(message.chat.id, 'User were sighed up!', reply_markup=markup)

@bot.callback_query_handler(func = lambda callback: True)
def callback(callback:types.CallbackQuery):

    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    userlist = cursor.fetchall()
    info = ''
    for el in userlist:
        info+= f'Username: {el[1]} Password: {el[2]}\n'
    cursor.close()
    connection.close()

    try:
        match callback.data:
            case 'userlist':  
                if not info:
                    bot.answer_callback_query(callback.id, text = "Processing")
                    bot.send_message(callback.message.chat.id, text = "List is empty.")
                else:
                    bot.answer_callback_query(callback.id, text = "Processing")
                    bot.send_message(callback.message.chat.id, text = info)
                    
                
            
            case 'clearlist':
                  
                bot.answer_callback_query(callback.id, text = "Processing")  
                connection = sqlite3.connect('database.sql')
                cursor = connection.cursor()
                
                cursor.execute("UPDATE users SET name = NULL")
                cursor.execute("UPDATE users SET password = NULL")
                cursor.execute("DELETE FROM users WHERE name IS NULL AND password IS NULL")
                connection.commit()
                cursor.close()
                connection.close()

                bot.send_message(callback.message.chat.id, text='User List was cleared.')
                

            case 'privacy':
                bot.answer_callback_query(callback.id, text = "Processing")
                bot.send_message(callback.message.chat.id, text = 'Privacy Template.', parse_mode='html')
                
            case 'help':
                bot.answer_callback_query(callback.id, text = "Processing")
                bot.send_message(callback.message.chat.id, text = '<b>Help Panel.</b>\n\nI can help you to manage chats and groups in <b>Telegram.</b>\n\n<b>Use these commands to control me:</b>\n<b> - /ban</b> to ban member.\n<b> - /mute</b> to restrict user from sending messages and media.\n<b> - /unban</b> delete user from banlist.\n<b> - /unmute</b> delete message restrictions for user.\n<b> - /serverstats</b> show server statistics.\n<b> - /pin</b> pin message.\n<b> - /unpin</b> unpin message.\n<b> - /unpinall</b> unpin all pinned messages.\n<em>///- in Progress</em>',parse_mode='html')
                
            case _:
                bot.answer_callback_query(callback.id, text = "Processing")
                bot.send_message(callback.message.chat.id, text="Unexpected Error.")
                
    except AttributeError:
        bot.send_message(callback.message.chat.id, text = f'Please select a message first.')

#COMMANDS

@bot.message_handler(commands=['help'])
def help(message:types.Message):
    bot.send_message(message.chat.id,'<b>Help Panel.</b>\n\nI can help you to manage chats and groups in <b>Telegram.</b>\n\n<b>Use these commands to control me:</b>\n<b> - /ban</b> to ban member.\n<b> - /mute</b> to restrict user from sending messages and media.\n<b> - /unban</b> delete user from banlist.\n<b> - /unmute</b> delete message restrictions for user.\n<b> - /serverstats</b> show server statistics.\n<b> - /pin</b> pin message.\n<b> - /unpin</b> unpin message.\n<b> - /unpinall</b> unpin all pinned messages.\n<em>///- in Progress</em>',parse_mode='html')

@bot.message_handler(commands=['rban'])
def rban(message:types.Message):
    try:
        reason = str(message.text[6:])
        if ('admchathelper_bot') in reason:
            reason =str(message.text[23:])
        bot.ban_chat_member(message.chat.id, user_id = message.reply_to_message.from_user.id, revoke_messages = True)
        bot.send_message(message.chat.id, text = f'User: @{bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.username} was banned from the server.\nReason: {reason}.\nResponsible Administrator: @{message.from_user.username}')
    except AttributeError:
        bot.send_message(message.chat.id, text = f'Please select a message first.')

#NONE_REPLY BAN
#@bot.message_handler(commands=['ban'])
#def ban(message:types.Message):
#    bot.ban_chat_member(message.chat.id, )

@bot.message_handler(commands=['unban'])
def unban(message:types.Message):
    try:
        bot.unban_chat_member(message.chat.id, user_id = message.reply_to_message.from_user.id,only_if_banned=True)
        bot.send_message(message.chat.id, text = f'User: @{bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.username} was unbanned by Administrator.\nResponsible Administrator: @{message.from_user.username}')
    except AttributeError:
        bot.send_message(message.chat.id, text = f'Please select a message first.')

@bot.message_handler(commands=['mute'])
def mute(message:types.Message):
    try:
        reason = str(message.text[6:])
        if ('admchathelper_bot') in reason:
            reason =str(message.text[23:])
        bot.restrict_chat_member(message.chat.id, user_id= message.reply_to_message.from_user.id, can_send_messages = False, can_send_media_messages=False, can_pin_messages=False, can_send_polls= False, can_change_info=False, can_add_web_page_previews=False, can_invite_users=False, can_send_other_messages=False)
        bot.send_message(message.chat.id, text=f'User: @{bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.username} was muted on the server.\nReason: {reason}.\nResponsible Administrator: @{message.from_user.username}')
    except AttributeError:
        bot.send_message(message.chat.id, text = f'Please select a message first.')

@bot.message_handler(commands=['unmute'])
def unmute(message:types.Message):
    try:
        bot.restrict_chat_member(message.chat.id, user_id= message.reply_to_message.from_user.id, can_send_messages = True, can_send_media_messages=True, can_send_polls=True,can_send_other_messages=True, can_add_web_page_previews= True, can_change_info=True,can_invite_users=True,can_pin_messages=True)
        bot.send_message(message.chat.id, text=f'User: @{bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.username} was unmuted by Administrator.\nResponsible Administrator: @{message.from_user.username}')
    except AttributeError:
        bot.send_message(message.chat.id, text = f'Please select a message first.')

@bot.message_handler(commands=['serverstats'])
def serverstats(message:types.Message):
    memberscount = bot.get_chat_members_count(message.chat.id)
    bot.send_message(message.chat.id, text=f"Stats:\nThere is {memberscount} members on the server at the moment.\n Administrators:\n{'\n'.join('@'+admin.user.username for admin in bot.get_chat_administrators(message.chat.id))}.")
    
@bot.message_handler(commands=['pin'])
def pin(message:types.Message):
    try:
        message_id = message.reply_to_message.message_id    
        bot.pin_chat_message(chat_id = message.chat.id, message_id = message_id)
        bot.send_message(chat_id = message.chat.id, text=f'Message {message_id} was pinned by Administrator.')
    except AttributeError:
        bot.send_message(message.chat.id, text = f'Please select a message first.')

@bot.message_handler(commands=['unpin'])
def unpin(message:types.Message):
    try:
        message_id = message.reply_to_message.message_id
        bot.unpin_chat_message(chat_id = message.chat.id, message_id = message_id)
        bot.send_message(chat_id = message.chat.id, text=f'Message {message_id} was unpinned by Administrator.')
    except AttributeError:
        bot.send_message(message.chat.id, text = f'Please select a message first.')

@bot.message_handler(commands=['unpinall'])
def unpinall(message:types.Message):
    bot.unpin_all_chat_messages(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='All messages were unpinned by Administrator.')


bot.polling(none_stop=True)