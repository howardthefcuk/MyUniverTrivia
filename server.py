import config
import telebot
import api_wrapper
from telebot import types

t = api_wrapper.Test("15692")



bot = telebot.TeleBot(config.token)
inQuestion = False


whynot = 'Why not?'
greeting = 'Hi, this is My Univer Daily Trivia Bot\n\nTap the button below if you want ot start'
nextOne = 'Nice one, take me to the next'
killBot = 'Kill the bot and \nsend me to the registration'
rightAnswer = 'That\'s Right!'
wrongAnswer = 'OH, I\'m affraid, not\nThe right answer is: '
addvert = 'It was a pleasure to deal with you, \ntry the full version of this educationall app on www.nahui.com'

@bot.message_handler(content_types=['text'])
def question(message):
	global inQuestion
	if message.text=="/start":
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
		bot.send_message(message.chat.id, addvert,reply_markup=markup)	
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

if __name__ == '__main__':
    bot.polling(none_stop=True)