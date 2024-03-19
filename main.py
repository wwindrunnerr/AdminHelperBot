import telebot
import os

from telebot import types 
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
user_id = os.environ['USER_ID']



@bot.message_handler(commands = ['start'])
def start(message):
    helpbtn = types.InlineKeyboardButton(text = 'Help', callback_data = 'help')
    markup = types.InlineKeyboardMarkup([[helpbtn]])
    bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name}!\nWhat`s our next step?', reply_markup = markup)

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id,'<b>Help Panel.</b>\n\nI can help you to manage chats and groups in <b> Telegram.</b>\n\n<b>Use these commands to control me:</b>\n<b> - /ban</b> to ban member.\n<em>///- in Progress</em>',parse_mode='html')

@bot.message_handler(commands = ['ban'])
def ban(message):
    bot.ban_chat_member(message.chat.id, user_id = user_id, revoke_messages = True)
    bot.send_message(message.chat.id, text = f'User: {user_id} was banned from the server.')

@bot.message_handler(commands = ['unban'])
def unban(message):
    bot.unban_chat_member(message.chat.id, user_id = user_id,only_if_banned=True)
    bot.send_message(message.chat.id, text = f'Administrator has unbanned user: {user_id}.')

@bot.message_handler(commands = ['mute'])
def mute(message):
    bot.restrict_chat_member(message.chat.id, user_id= user_id, can_send_messages = False, can_send_media_messages=False, can_pin_messages=False, can_send_polls= False, can_change_info=False, can_add_web_page_previews=False, can_invite_users=False, can_send_other_messages=False)
    bot.send_message(message.chat.id, text=f'User: {user_id} was muted.')

@bot.message_handler(commands=['unmute'])
def unmute(message):
    bot.restrict_chat_member(message.chat.id, user_id= user_id, can_send_messages = True, can_send_media_messages=True, can_send_polls=True,can_send_other_messages=True, can_add_web_page_previews= True, can_change_info=True,can_invite_users=True,can_pin_messages=True)
    bot.send_message(message.chat.id, text=f'User: {user_id} was unmuted.')

#@bot.message_handler(commands=['adduser'])
#def adduser(message):
#    bot.add_chat_member_handler()

@bot.callback_query_handler(func = lambda callback: True)
def helpcallback(callback):
    if callback.data == 'help':
        bot.send_message(callback.message.chat.id, text = '<b>Help Panel.</b>\n\nI can help you to manage chats and groups in <b> Telegram.</b>\n\n<b>Use these commands to control me:</b>\n.<b>/ban</b> to ban member.\n<em>///- in Progress</em>',parse_mode='html')

bot.polling(none_stop=True)