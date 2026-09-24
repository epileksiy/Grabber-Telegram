import telebot
import json

bot = telebot.TeleBot()
print('::Bot is running::')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Anime for gays")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	print(message.text)
	bot.send_message(message.chat.id, 'Нормально выдал, мужик, твоё сообщение: "' + message.text +'"')

# bot.send_message( -1001504897499, 'Соси')

# @bot.channel_post_handler(func=lambda message:  True)
# def echo_all2(message):
# 	print(message.text)
# 	bot.send_message(message.chat.id, 'Нормалььно общайся, лох, гуляй')


@bot.channel_post_handler(func=lambda message: message.text == 'messages')
def echo_all2(message):
	print(message.text)
	# bot.send_message(message.chat.id, 'Бот 🤖: Да, окей. 🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖')


try:
	pending_updates = bot.get_updates()

	for pending_request in pending_updates:
		print('Pending Request', pending_request)
except Exception:
	print('che')
	print(Exception)

bot.infinity_polling()
