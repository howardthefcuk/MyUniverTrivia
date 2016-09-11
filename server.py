# Encoding: UTF-8 

import config
import telebot
import api_wrapper
import schedule
import time
from telebot import types

t = api_wrapper.Test("15692")



bot = telebot.TeleBot(config.token)
inQuestion = False

usid = ''

whynot = 'Почему бы и нет?'
greeting = 'Привет! Это бот с ежедневными вопросами портала МойУнивер\n\nНажми на кнопку ниже, если хочешь начать'
nextOne = 'Чудно, дай мне еще вопрос'
killBot = 'Нет, спасибо, хватит.'
rightAnswer = 'Правильно!'
wrongAnswer = 'Ох, боюсь, нет. Правильный ответ: '
addvert = 'Было очень приятно с тобой играть, \nэта тривиа построена на основе курсов с сайта Мой Универ'
addvertMore = 'Посмотри, может найдешь что-нибудь интересное для себя ;)'
dailyMessage = 'Пришло время нового ежедневного вопроса!' 
noDaily = 'Больше не получать ежедневных вопросов'
finalAddvert = 'Окей, спасибо за игру'

@bot.message_handler(content_types=['text'])
def ask(message):
	global usid
	global inQuestion
	if message.text=="/start":
		usid = message.chat.id
		markup = types.ReplyKeyboardMarkup(row_width=1)
		markup.add(whynot)
		bot.send_message(message.chat.id, greeting,reply_markup=markup)
	elif inQuestion:
		res = t.validate_answer(int(message.text)-1)
		markup = types.ReplyKeyboardHide(selective=False)
		markup = types.ReplyKeyboardMarkup(row_width=1)
		markup.add(nextOne)
		markup.add(killBot)
		if res['right']:
			bot.send_message(message.chat.id, rightAnswer,reply_markup=markup)
		else:
			bot.send_message(message.chat.id, wrongAnswer+res['right_answer'],reply_markup=markup)	
		inQuestion = False
	elif message.text==killBot:
		markup = types.ReplyKeyboardHide(selective=False)
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		url_button1 = types.InlineKeyboardButton(text="iOS", url="https://itunes.apple.com/ru/app/moj-univer/id656335236?mt=8")
		url_button2 = types.InlineKeyboardButton(text="WP", url=r"https://www.microsoft.com/en-us/store/p/%D0%9C%D0%BE%D0%B9-%D0%A3%D0%BD%D0%B8%D0%B2%D0%B5%D1%80/9wzdncrdkknr")
		url_button3 = types.InlineKeyboardButton(text="Android", url="https://play.google.com/store/apps/details?id=ru.etemplarsoft.mu.main.pro")
		keyboard.add(url_button1,url_button2,url_button3)
		bot.send_message(message.chat.id, addvert, reply_markup=markup)
		bot.send_message(message.chat.id, addvertMore, reply_markup=keyboard)	
		time.sleep(10)
		dailik()
	elif message.text== noDaily:
		markup = types.ReplyKeyboardHide(selective=False)
		bot.send_message(message.chat.id, finalAddvert, reply_markup=markup)
	else:
		markup = types.ReplyKeyboardMarkup(row_width=2)
		markup.add('1', '2', "3",'4')
		questions = t.get_next_question()
		final_string = ''
		final_string += questions.question_text + '\n\n'
		for i,k in enumerate(questions.answer_strings):
			final_string += str(i+1)+") " + k + "\n"
		bot.send_message(message.chat.id, final_string ,reply_markup=markup)
		inQuestion = True

def dailik():
	global inQuestion
	bot.send_message(usid, dailyMessage)
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('1', '2', "3",'4',noDaily)
	questions = t.get_next_question()
	final_string = ''
	final_string += questions.question_text + '\n\n'
	for i,k in enumerate(questions.answer_strings):
		final_string += str(i+1)+") " + k + "\n"
	bot.send_message(usid, final_string ,reply_markup=markup)
	inQuestion = True



if __name__ == '__main__':
	#schedule.every(1).day.do(dailik)
	bot.polling(none_stop=True)
	#while True:
	#	schedule.run_pending()
	#	time.sleep(1)
	
