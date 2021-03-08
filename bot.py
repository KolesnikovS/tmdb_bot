import telebot
from telebot import types
import urllib.request
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = 'YOUR_TMDB_API_KEY'
tmdb.language = 'en'
tmdb.debug = True

token = 'YOUR_TELEGRAM_TOKEN'
base_movie_url="https://your.streaming.service/"
tmdb_photo_url="http://image.tmdb.org/t/p/w500"


bot = telebot.TeleBot(token)


def send_film_card(message, text, film_no):
	chat_id = message.chat.id
	movie = Movie()
	search = movie.search(text)
	if(search):
		res = search[film_no]
		if(res):
			film_id = res.id
			url = base_movie_url + str(film_id)
			#different keyboards
			keyboard_first = types.InlineKeyboardMarkup()
			keyboard_last = types.InlineKeyboardMarkup()
			keyboard_middle = types.InlineKeyboardMarkup()
			keyboard_single = types.InlineKeyboardMarkup()
			item_prev = types.InlineKeyboardButton(text='<-', callback_data=text+' '+str(film_no-1))
			item = types.InlineKeyboardButton(text='Смотреть', url = url)
			item_next = types.InlineKeyboardButton(text='->', callback_data=text+' '+str(film_no+1))
			keyboard_first.add( item, item_next)
			keyboard_middle.add(item_prev, item, item_next)
			keyboard_last.add(item_prev, item)
			keyboard_single.add(item)
			#checking which keyboard to use
			if(int(len(search)) == 1):
				keyboard = keyboard_single
			elif (film_no == 0):
				keyboard = keyboard_first
			elif (film_no == len(search)-1):
				keyboard = keyboard_last
			else:
				keyboard = keyboard_middle
			url = fsapi_movie_url + str(res.id)
			photo_text = "*" + str(res.title) + "* \n\n" + \
					res.overview
			if(len(photo_text)>380:
				photo_text = photo_text[0:380] + "..."
			photo_text += "\n\nрейтинг: " + str(res.vote_average)
			if(res.poster_path):					
				photo_url = tmdb_photo_url + res.poster_path
				
				bot.send_photo(chat_id, photo_url, caption = photo_text, reply_markup=keyboard, parse_mode = "Markdown")
			else:
				bot.send_message(chat_id, photo_text, reply_markup=keyboard, parse_mode = "Markdown")

	else:
		bot.send_message(chat_id, "Ничего не нашлось")




#кнопка /cancel
@bot.message_handler(commands=['start'])
def cancel(message):
	bot.send_message(message.chat.id, "Какой фильм ищем?")




#получили название
@bot.message_handler(func=lambda m: True)
def handle_text_hoto(message):
	chat_id = message.chat.id
	text = message.text
	movie = Movie()
	search = movie.search(text)
	if(search):
		film_no = 0
		res = search[0]
		film_id = res.id
		send_film_card(message, text, film_no)
	else:
		bot.send_message(chat_id, "Ничего не нашлось")

#Конкретный фильм
@bot.callback_query_handler(func=lambda call: True)
def film_card(call):
	call_data = call.data.split()
	film_no = int(call_data[-1])
	del call_data[-1]
	text = " ".join(call_data)
	send_film_card(call.message, text, film_no)
	bot.delete_message(call.message.chat.id, call.message.message_id)




if __name__ == "__main__":
    bot.infinity_polling()
