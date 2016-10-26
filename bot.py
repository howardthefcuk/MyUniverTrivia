import telebot
import config
import collections
import api_wrapper
import schedule
import time
from telebot import types
import threading
import os
from flask import Flask, request

server = Flask(__name__)
bot = telebot.TeleBot(config.token)
t = api_wrapper.Test("15692")


class buddy:
	
	def __init__(self, botik):
		self.users = collections.defaultdict(int)
		self.bot = botik 
		self.whynot = 'Почему бы и нет?'	
		self.greeting = 'Привет! Это бот с ежедневными вопросами портала МойУнивер\n\nНажми на кнопку ниже, если хочешь начать'
		self.nextOne = 'Чудно, дай мне еще вопрос'
		self.killBot = 'Нет, спасибо, хватит.'
		self.rightAnswer = 'Правильно!'
		self.wrongAnswer = 'Ох, боюсь, нет. Правильный ответ: '
		self.addvert = 'Было очень приятно с тобой играть, \nэта тривиа построена на основе курсов с сайта Мой Универ'
		self.addvertMore = 'Посмотри, может найдешь что-нибудь интересное для себя ;)'
		self.dailyMessage = 'Пришло время нового ежедневного вопроса!' 
		self.noDaily = 'Больше не получать ежедневных вопросов'
		self.finalAddvert = 'Окей, спасибо за игру'
		self.errorMessage = 'Ошибка. Введите, пожалуйста номер ответа.'
		self.annoy = False

	def getState(self, user):
		return self.users[user]


	def lifetime(self, message):
		temp = message.chat.id
		print('Logging. user: ' + str(message.chat.id) + ' state ' + str(self.getState(message.chat.id)))
		if self.users[temp]==0:
			self.users[temp] = self.actionState0(message)
		elif self.users[temp]==1:
			self.users[temp] = self.actionState1(message)
		elif self.users[temp]==2:
			self.users[temp] = self.actionState2(message)

	def actionState0(self, message):
		usid = message.chat.id
		markup = types.ReplyKeyboardMarkup(row_width=1)
		markup.add(self.whynot)
		bot.send_message(message.chat.id, self.greeting,reply_markup=markup)
		return 1

	def actionState1(self, message):
		if message.text == self.killBot:
			markup = types.ReplyKeyboardHide(selective=False)
			keyboard = types.InlineKeyboardMarkup(row_width=3)
			url_button1 = types.InlineKeyboardButton(text="iOS", url="https://itunes.apple.com/ru/app/moj-univer/id656335236?mt=8")
			url_button2 = types.InlineKeyboardButton(text="WP", url=r"https://www.microsoft.com/en-us/store/p/%D0%9C%D0%BE%D0%B9-%D0%A3%D0%BD%D0%B8%D0%B2%D0%B5%D1%80/9wzdncrdkknr")
			url_button3 = types.InlineKeyboardButton(text="Android", url="https://play.google.com/store/apps/details?id=ru.etemplarsoft.mu.main.pro")
			keyboard.add(url_button1,url_button2,url_button3)
			bot.send_message(message.chat.id, self.addvert, reply_markup=markup)
			bot.send_message(message.chat.id, self.addvertMore, reply_markup=keyboard)
		else:
			markup = types.ReplyKeyboardMarkup(row_width=2)
			markup.add('1', '2', "3",'4')
			questions = t.get_next_question()
			final_string = ''
			final_string += questions.question_text + '\n\n'
			for i,k in enumerate(questions.answer_strings):
				final_string += str(i+1)+") " + k + "\n"
			bot.send_message(message.chat.id, final_string ,reply_markup=markup)
		return 2
		
	def actionState2(self, message):
		try:
			res = t.validate_answer(int(message.text)-1)
		except:
			markup = types.ReplyKeyboardMarkup(row_width=2)
			markup.add('1', '2', "3",'4')
			bot.send_message(message.chat.id, self.errorMessage, reply_markup=markup)
			return 2
		markup = types.ReplyKeyboardHide(selective=False)
		markup = types.ReplyKeyboardMarkup(row_width=1)
		markup.add(self.nextOne)
		markup.add(self.killBot)
		if res['right']:
			bot.send_message(message.chat.id, self.rightAnswer,reply_markup=markup)
		else:
			bot.send_message(message.chat.id, self.wrongAnswer+res['right_answer'],reply_markup=markup)	
		inQuestion = False
		return 1

	def timerAction(self):
		while True:
			if self.annoy:
				break
			if time.ctime().split()[3].split(':')[1] == '09':
				bot.send_message(usid, dailyMessage)
				markup = types.ReplyKeyboardMarkup(row_width=2)
				markup.add('1', '2', "3",'4',noDaily)
				questions = t.get_next_question()
				final_string = ''
				final_string += questions.question_text + '\n\n'
				for i,k in enumerate(questions.answer_strings):
					final_string += str(i+1)+") " + k + "\n"
				bot.send_message(usid, final_string ,reply_markup=markup)
				time.sleep(10)
				self.users[usid] = 2
			time.sleep(10)



@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://herokuProject_url/bot")
    return "!", 200


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    puppy.lifetime(message)
 
if __name__ == '__main__':
	puppy = buddy(bot)
	threading.Thread(target = server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
).start()
	threading.Thread(target = puppy.timerAction()).start()

