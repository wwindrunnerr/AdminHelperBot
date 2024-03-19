import telebot
import os

from telebot import types 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

load_dotenv()

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
#user_id = os.environ['USER_ID']



@bot.message_handler(commands=['start'])
def start(message:types.Message):
    helpbtn = types.InlineKeyboardButton(text = 'Help', callback_data = 'help')
    markup = types.InlineKeyboardMarkup([[helpbtn]])
    bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name}!\nWhat`s our next step?', reply_markup = markup)

@bot.message_handler(commands=['help'])
def help(message:types.Message):
    bot.send_message(message.chat.id,'<b>Help Panel.</b>\n\nI can help you to manage chats and groups in <b>Telegram.</b>\n\n<b>Use these commands to control me:</b>\n<b> - /ban</b> to ban member.\n<b> - /mute</b> to restrict user from sending messages and media.\n<b> - /unban</b> delete user from banlist.\n<b> - /unmute</b> delete message restrictions for user.\n<b> - /serverstats</b> show server statistics.\n<b> - /pin</b> pin message.\n<b> - /unpin</b> unpin message.\n<b> - /unpinall</b> unpin all pinned messages.\n<em>///- in Progress</em>',parse_mode='html')

@bot.message_handler(commands=['ban'])
def ban(message:types.Message):
    bot.ban_chat_member(message.chat.id, user_id = message.reply_to_message.from_user.id, revoke_messages = True)
    bot.send_message(message.chat.id, text = f'User: {bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.full_name} was banned from the server.')

@bot.message_handler(commands=['unban'])
def unban(message:types.Message):
    bot.unban_chat_member(message.chat.id, user_id = message.reply_to_message.from_user.id,only_if_banned=True)
    bot.send_message(message.chat.id, text = f'User: {bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.full_name} was unbanned by Administrator.')

@bot.message_handler(commands=['mute'])
def mute(message:types.Message):
    bot.restrict_chat_member(message.chat.id, user_id= message.reply_to_message.from_user.id, can_send_messages = False, can_send_media_messages=False, can_pin_messages=False, can_send_polls= False, can_change_info=False, can_add_web_page_previews=False, can_invite_users=False, can_send_other_messages=False)
    bot.send_message(message.chat.id, text=f'User: {bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.full_name} was muted on the server.')

@bot.message_handler(commands=['unmute'])
def unmute(message:types.Message):
    bot.restrict_chat_member(message.chat.id, user_id= message.reply_to_message.from_user.id, can_send_messages = True, can_send_media_messages=True, can_send_polls=True,can_send_other_messages=True, can_add_web_page_previews= True, can_change_info=True,can_invite_users=True,can_pin_messages=True)
    bot.send_message(message.chat.id, text=f'User: {bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id).user.full_name} was unmuted by Administrator.')

@bot.message_handler(commands=['serverstats'])
def serverstats(message:types.Message):
    memberscount = bot.get_chat_members_count(message.chat.id)
    bot.send_message(message.chat.id, text=f"Stats:\nThere is {memberscount} members on the server at the moment.\n Administrators:\n{'\n'.join('@'+admin.user.username for admin in bot.get_chat_administrators(message.chat.id))}.")
    
@bot.message_handler(commands=['pin'])
def pin(message:types.Message):
   # if message.reply_to_message.message_id == None:
        #bot.send_message(chat_id= message.chat.id, text='You should select message first.')
    #else:
        message_id = message.reply_to_message.message_id    
        bot.pin_chat_message(chat_id = message.chat.id, message_id = message_id)
        bot.send_message(chat_id = message.chat.id, text=f'Message {message_id} was pinned by Administrator.')

@bot.message_handler(commands=['unpin'])
def unpin(message:types.Message):
    message_id = message.reply_to_message.message_id
    bot.unpin_chat_message(chat_id = message.chat.id, message_id = message_id)
    bot.send_message(chat_id = message.chat.id, text=f'Message {message_id} was unpinned by Administrator.')

@bot.message_handler(commands=['unpinall'])
def unpinall(message:types.Message):
    bot.unpin_all_chat_messages(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='All messages were unpinned by Administrator.')


#@bot.register_chat_member_handler(func = lambda callback:True)
#def adduser(callback)

#@bot.message_handler(commands=['adduser'])
#def adduser(message):
#    bot.add_chat_member_handler()

@bot.callback_query_handler(func = lambda callback: True)
def helpcallback(callback):
    if callback.data == 'help':
        bot.send_message(callback.message.chat.id, text = '<b>Help Panel.</b>\n\nI can help you to manage chats and groups in <b>Telegram.</b>\n\n<b>Use these commands to control me:</b>\n<b> - /ban</b> to ban member.\n<b> - /mute</b> to restrict user from sending messages and media.\n<b> - /unban</b> delete user from banlist.\n<b> - /unmute</b> delete message restrictions for user.\n<b> - /serverstats</b> show server statistics.<b> - /pin</b> pin message.<b> - /unpin</b> unpin message.<b> - /unpinall</b> unpin all pinned messages.<em>///- in Progress</em>',parse_mode='html')

bot.polling(none_stop=True)