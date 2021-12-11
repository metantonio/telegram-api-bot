import time
import schedule
import os
import telebot # Importamos las librería
#from http.client import httplib
#from urllib.parse import urlparse, parse_qs
import requests
from lxml import html
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from os import path, stat, remove, makedirs
from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)
from telethon.errors import SessionPasswordNeededError
import json
import pandas as pd

from collections import OrderedDict
####################################################################################################

### Constants ###

# Client parameters
API_ID   = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
PHONE_NUM    = os.environ.get("PHONE_NUM")

# Chat to inspect
CHAT_LINK  = os.environ.get("CHAT_LINK")
GROUP_NAME = "MigrActiva"

subjectFilter = ['Saren','#Saren','SAREN','#SAREN']
levelFilter = ['Citas','citas']

client = TelegramClient('session', API_ID, API_HASH)
####################################################################################################
### Telegram basic functions ###

# Connect and Log-in/Sign-in to telegram API
def tlg_connect(api_id, api_hash, phone_number):
	'''Connect and Log-in/Sign-in to Telegram API. Request Sign-in code for first execution'''
	print('Trying to connect to Telegram...')
	client = TelegramClient("Session", api_id, api_hash)
	if not client.start():
		print('Could not connect to Telegram servers.')
		return None
	else:
		if not client.is_user_authorized():
			print('Session file not found. This is the first run, sending code request...')
			client.sign_in(phone_number)
			self_user = None
			while self_user is None:
				code = input('Enter the code you just received: ')
				try:
					self_user = client.sign_in(code=code)
				except SessionPasswordNeededError:
					pw = getpass('Two step verification is enabled. Please enter your password: ')
					self_user = client.sign_in(password=pw)
					if self_user is None:
						return None
	print('Sign in success.')
	print()
	return client


# Get basic info from a chat
def tlg_get_basic_info(client, chat):
	'''Get basic information (id, title, name, num_users, num_messages) from a group/channel/chat'''
	# Get the corresponding chat entity
	chat_entity = client.get_entity(chat)
	# Get the number of users in the chat
##	num_members_offset = client(GetParticipantsRequest(channel=chat_entity, \
##		filter=ChannelParticipantsSearch(''), offset=0, limit=0, hash=0)).count
##	num_members = client(GetParticipantsRequest(channel=chat_entity, \
##		filter=ChannelParticipantsSearch(''), offset=num_members_offset, limit=0, hash=0)).count
	# Get messages data from the chat and extract the usefull data related to chat
	msgs = client.get_messages(chat_entity, limit=1)
	basic_info = OrderedDict \
		([ \
			("id", msgs[0].chat_id), \
			("title", msgs[0].chat.title), \
			("username", msgs[0].chat.username), \
			#("num_members", num_members), \
			("num_messages", msgs.total), \
			("supergroup", msgs[0].chat.megagroup) \
		])
	# Return basic info dict
	return basic_info


# Get all members data from a chat
def tlg_get_all_members(client, chat):
	'''Get all members information from a group/channel/chat'''
	# Get the corresponding chat entity
	chat_entity = client.get_entity(chat)
	# Get and save all users data in a single list
	i = 0
	members = []
	users = []
	num_members = client(GetParticipantsRequest(channel=chat_entity, \
		filter=ChannelParticipantsSearch(''), offset=0, limit=0, hash=0)).count
	while True:
		participants_i = client(GetParticipantsRequest(channel=chat_entity, \
			filter=ChannelParticipantsSearch(''), offset=i, limit=num_members, hash=0))
		if not participants_i.users:
			break
		users.extend(participants_i.users)
		i = i + len(participants_i.users)
	# Build our messages data structures and add them to the list
	for usr in users:
		usr_last_connection = ""
		if hasattr(usr.status, "was_online"):
			usr_last_connection = "{}/{}/{} - {}:{}:{}".format(usr.status.was_online.day, \
				usr.status.was_online.month, usr.status.was_online.year, \
				usr.status.was_online.hour, usr.status.was_online.minute, \
				usr.status.was_online.second)
		else:
			usr_last_connection = "The user does not share this information"
		usr_data = OrderedDict \
			([ \
				("id", usr.id), \
				("username", usr.username), \
				("first_name", usr.first_name), \
				("last_name", usr.last_name), \
				("last_connection", usr_last_connection) \
			])
		members.append(usr_data)
	# Return members list
	return members


# Get messages data from a chat
def tlg_get_messages(client, chat, num_msg):
	'''Get all members information from a group/channel/chat'''
	# Set the result list
	messages = []
	# Get the corresponding chat entity
	chat_entity = client.get_entity(chat)
	# Get and save messages data in a single list
	msgs = client.get_messages(chat_entity, limit=num_msg)
	# Build our messages data structures and add them to the list
	for msg in reversed(msgs.data):
		msg_sender = msg.sender.first_name
		if msg.sender.last_name:
			msg_sender = "{} {}".format(msg_sender, msg.sender.last_name)
		if msg.sender.username:
			msg_sender = "{} ({})".format(msg_sender, msg.sender.username)
		msg_sent_date = "{}/{}/{}".format(msg.date.day, msg.date.month, msg.date.year)
		msg_sent_time = "{}:{}:{}".format(msg.date.hour, msg.date.minute, msg.date.second)
		msg_data = OrderedDict \
			([ \
				("id", msg.id), ("text", msg.message), ("sent_time", msg_sent_time), \
				("sent_date", msg_sent_date), ("sender_user", msg_sender), \
				("sender_user_id", msg.sender.id), ("reply_to", msg.reply_to_msg_id) \
			])
		messages.append(msg_data)
	# Return the messages data list
	return messages


# Get all messages data from a chat
def tlg_get_all_messages(client, chat):
	'''Get all members information from a group/channel/chat'''
	# Set the result list
	messages = []
	# Get the corresponding chat entity
	chat_entity = client.get_entity(chat)
	# Get and save all messages data in a single list
	num_msg = client.get_messages(chat_entity, limit=100)
	msgs = client.get_messages(chat_entity, limit=100)
	# Build our messages data structures and add them to the list
	for msg in reversed(msgs):
            #print('sender:', msg.sender)                
            msg_sender = msg.sender.username
##            if msg.sender.last_name:
##                    msg_sender = "{} {}".format(msg_sender, msg.sender.username)
            if msg.sender.username:
                    msg_sender = "{} (@{})".format(msg_sender, msg.sender.username)
            msg_sent_date = "{}/{}/{}".format(msg.date.day, msg.date.month, msg.date.year)
            msg_sent_time = "{}:{}:{}".format(msg.date.hour, msg.date.minute, msg.date.second)
            msg_data = OrderedDict \
                    ([ \
                            ("id", msg.id), ("text", msg.message), ("sent_time", msg_sent_time), \
                            ("sent_date", msg_sent_date), ("sender_user", msg_sender), \
                            ("sender_user_id", msg.sender.id), ("reply_to", msg.reply_to_msg_id) \
                    ])
            messages.append(msg_data)
	# Return the messages data list
	return messages
def all_msg(client, group_username):
        chats =client.get_messages(group_username, limit=100) # n number of messages to be extracted
        # Get message id, message, sender id, reply to message id, and timestamp
        message_id =[]
        message =[]
        sender =[]
        reply_to =[]
        time = []
        if len(chats):
            for chat in chats:
                message_id.append(chat.id)
                message.append(chat.message)
                sender.append(chat.from_id)
                reply_to.append(chat.reply_to_msg_id)
                time.append(chat.date)
        data ={'message_id':message_id, 'message': message, 'sender_ID':sender, 'reply_to_msg_id':reply_to, 'time':time}
        df = pd.DataFrame(data)
        print(df)
        return data

def specific_msg(client, group_username, keyword):
        messages =[]
        time = []
        for message in client.iter_messages(group_username, search=keyword):
            messages.append(message.message) # get messages 
            time.append(message.date) # get timestamp
        data ={'time':time, 'message':messages}

        df = pd.DataFrame(data)
        print(df)
        return data


####################################################################################################

### Json files handle functions ###

def json_write(file, data):
	'''Write element data to content of JSON file'''
	# Add the data to a empty list and use the write_list function implementation
	data_list = []
	data_list.append(data)
	json_write_list(file, data_list)


def json_write_list(file, list):
	'''Write all the list elements data to content of JSON file'''
	try:
		# Create the directories of the file path if them does not exists
		directory = path.dirname(file)
		if not path.exists(directory):
			makedirs(directory)
		# If the file does not exists or is empty, write the JSON content skeleton
		if not path.exists(file) or not stat(file).st_size:
			with open(file, "w", encoding="utf-8") as f:
				f.write('\n{\n    "Content": []\n}\n')
		# Read file content structure
		with open(file, "r", encoding="utf-8") as f:
			content = json.load(f, object_pairs_hook=OrderedDict)
		# For each data in list, add to the json content structure
		for data in list:
			if data:
				content['Content'].append(data) # Añadir los nuevos datos al contenido del json
		# Overwrite the JSON file with the modified content data
		with open(file, "w", encoding="utf-8") as f:
			json.dump(content, fp=f, ensure_ascii=False, indent=4)
	# Catch and handle errors
	except IOError as e:
		print("    I/O error({0}): {1}".format(e.errno, e.strerror))
	except ValueError:
		print("    Error: Can't convert data value to write in the file")
	except MemoryError:
		print("    Error: You are trying to write too much data")

####################################################################################################


TOKEN=os.environ.get("TOKEN") # Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN)  #Creamos nuestra instancia "bot" a partir de ese TOKEN
idGrupoFrom = os.environ.get("IDMIGRA")
#Grupo del SAREN/SAIME
chat_id = os.environ.get("CHAT_ID")
user = bot.get_me()
#print(user)
#Es equivalente a esto 
#https://api.telegram.org/bot<TU_TOKEN>/getMe



#Es equivalente a esto 
#https://api.telegram.org/bot<TU_TOKEN/getUpdates

def enviarMensaje(mensaje, igGrupo):
    requests.post('https://api.telegram.org/bot' + TOKEN + '/sendMessage', data={'chat_id': idGrupo, 'text': mensaje, 'parse_mode': 'HTML'})
    
def enviarDocumento(ruta, idGrupo):
    requests.post('https://api.telegram.org/bot' + TOKEN + '/sendDocument',
              files={'document': (ruta, open(ruta, 'rb'))},
              data={'chat_id': idGrupo, 'caption': 'imagen caption'})

def echo(update, context):
    print("test")
        
def start(update,context):
    myBot=context.bot
    
    

#bot.send_message(chat_id, "Mensaje automático de prueba") ##envío del mensaje
#print(chat_id)

def test():
    return print("test")

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    #myBot = context.bot
    updateMsg = getattr(updater, 'message', None)
    messageId = updateMsg.message_id
    chatId = update.message.chat_id
    print('chatId: ', chatId)
    userName = update.message.chat_id
    text= update.message.text
    #logger.info(f'El usuario {userName} ha emitido un mensaje al grupo {chatId}')

    saren = 'Saren'
    #print('por entrar al if')
    if saren in text:
        #bot.send_message(chat_id, "Citas del Saren Disponibles!!! Pagina:https://citas.saren.gob.ve")
        print('Citas del Saren Disponibles!!! Pagina:https://citas.saren.gob.ve')
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    
###################################################################
CHAT_LINK_test = 'https://t.me/metantonio' #es el link de un usuario/canal registrado que escriba con ese username
chat_id_prueba = "-617728644"
CHAT_LINK_DESTINO=os.environ.get("CHAT_LINK_DESTINO")
bot = telebot.TeleBot(TOKEN)
user = bot.get_me()
updates=bot.get_updates()


@client.on(events.NewMessage(chats=CHAT_LINK))
async def newMessageListener(event):
        updates=bot.get_updates()
        newMessage = event.message.message
        print(newMessage)
        #print(event.raw_text)
        await client.forward_messages(entity=CHAT_LINK_DESTINO, messages=event.message)
        bot.send_message(chat_id, "prueba")
##with client:
##        client.run_until_disconnected()
        
### Main function ###
def mainclient():
	'''Main Function'''
	print()
	# Create the client and connect
	#client = tlg_connect(API_ID, API_HASH, PHONE_NUM)
	if client is not None:
            # Get chat basic info
            print('Getting chat basic info...')
            chat_info = tlg_get_basic_info(client, CHAT_LINK)
    ##      chat_info={}
            # Create output JSON files from basic info chat name
            if chat_info["username"]:
                files_name = chat_info["username"]
            else:
                files_name = chat_info["id"]
            fjson_chat = "./output/{}/chat.json".format(files_name) # Chat basic info json file
            fjson_users = "./output/{}/users.json".format(files_name) # Chat basic info json file
            fjson_messages = "./output/{}/messages.json".format(files_name) # Chat basic info json file

        # Save chat basic info to the output file
            if path.exists(fjson_chat):
                remove(fjson_chat)
            json_write(fjson_chat, chat_info)

            # Get all users data from the chat and save to the output file
##            print('Getting chat members (users) info...')
##            members = tlg_get_all_members(client, CHAT_LINK)
##            if path.exists(fjson_users):
##                remove(fjson_users)
##            json_write_list(fjson_users, members)

            # Get all messages data from the chat and save to the output file
            print('Getting chat messages info...')
            messages = tlg_get_all_messages(client, CHAT_LINK)
            #fjson_messages = "./output/{}/messages.json".format("grupo") # Chat basic info json file
            if path.exists(fjson_messages):
                remove(fjson_messages)
            json_write_list(fjson_messages, messages)

            print('Proccess completed')
            all_msg(client,"MigrActiva")
            specific_msg(client,"MigrActiva","Saren") #needs client, group_name, keyword to search
            print()
##            @client.on(events.NewMessage(chats=GROUP_NAME))
##            async def my_event_handler(event):
##                print(event.raw_text)
#client = tlg_connect(API_ID, API_HASH, PHONE_NUM)            

####################################################################################################    

if __name__== "__main__" :
    print("Iniciando")
    with client:
            bot.send_message(chat_id_prueba, "Mensaje automático de prueba")
            mainclient()
            client.run_until_disconnected()


##    schedule.every(1).minutes.do(test) #schedule sólo puede llamar a funciones definidas por el usuario
##    while True:
##        schedule.run_pending()
##        time.sleep(1)
