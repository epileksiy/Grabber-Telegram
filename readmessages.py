import json  # подключили библиотеку для работы с json
from grabber import main,client,username

import configparser
import json
# import sys
#
# # reload(sys)
#
# sys.setdefaultencoding('utf8')

from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
import os
from flask import Flask

import nest_asyncio
nest_asyncio.apply()


# def parse_data(url):
#     # cwd = os.getcwd()
#     # print(cwd)
#     # # Out: c:\Users\esimm\PythonDev\notebooks
#     # filesArr = os.listdir(cwd)
#     # print('Current dir files: ', filesArr)
#
#     client.loop.run_until_complete(main(url))
#     # client.loop.create_task(main(url))
#
#     # if ((username + '.session') not in filesArr):
#     #     print('New session, please authentificate using authent.py')
#     # else:
#     #     print('  Authentificated  ')
#     #     client.loop.run_until_complete(main(url))
#

# async def dump_all_participants(channel):
# 	"""Записывает json-файл с информацией о всех участниках канала/чата"""
# 	offset_user = 0    # номер участника, с которого начинается считывание
# 	limit_user = 100   # максимальное число записей, передаваемых за один раз
#
# 	all_participants = []   # список всех участников канала
# 	filter_user = ChannelParticipantsSearch('')
#
# 	while True:
# 		participants = await client(GetParticipantsRequest(channel,
# 			filter_user, offset_user, limit_user, hash=0))
# 		if not participants.users:
# 			break
# 		all_participants.extend(participants.users)
# 		offset_user += len(participants.users)
#
# 	all_users_details = []   # список словарей с интересующими параметрами участников канала
#
# 	for participant in all_participants:
# 		all_users_details.append({"id": participant.id,
# 			"first_name": participant.first_name,
# 			"last_name": participant.last_name,
# 			"user": participant.username,
# 			"phone": participant.phone,
# 			"is_bot": participant.bot})
#
# 	with open('channel_users.json', 'w', encoding='utf8') as outfile:
# 		json.dump(all_users_details, outfile, ensure_ascii=False)


async def dump_all_messages(channel):
	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 100   # максимальное число записей, передаваемых за один раз

	all_messages = []
	total_messages = 0
	total_count_limit = 0

	class DateTimeEncoder(json.JSONEncoder):
		'''Класс для сериализации записи дат в JSON'''
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		 json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main(url):
	channel = await client.get_entity(url)
	# await dump_all_participants(channel)
	# print('started main')
	await dump_all_messages(channel)
	# print('ended main')

config = configparser.ConfigParser()
config.read("config.ini")

api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# proxy = (proxy_server, proxy_port, proxy_key)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/readmessages')
async def return_data():

    client = TelegramClient(username, api_id, api_hash)

    client.start()

    main('https://t.me/sadhighkid')

    data = []
    with open('channel_messages.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
        for i in text:
            try:
                # print(i['message'])
                data.append((i['message']))
            except:
                continue

    jsonData = dict.fromkeys(list(map(lambda x: str(x),range(len(data)))))

    for i in range(len(jsonData)):
        jsonData[str(i)]=data[i]

    # jsonData = json.dumps(jsonData)
    # print(jsonData)

    return jsonData

if __name__ == "__main__":
    app.run()
