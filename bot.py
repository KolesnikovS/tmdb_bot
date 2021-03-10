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


def err(text):
    print(text + " error")


# movie card
def send_film_card(message, text, film_no):
    chat_id = message.chat.id
    movie = Movie()
    search = movie.search(text)
    if (search):
        res = search[film_no]
        res = (movie.details(res.id))
        if res and res:
            film_id = res.id
            url = base_movie_url + str(film_id)
            try:
                genres = []
                genres_list = res.genres
                for genre in genres_list:
                    genres.append(genre.name)
                genres = genres[0:4]
                genres = ",".join(genres)
            except:
                genres = ""
            try:
                release_date = res.release_date[0:4]
            except:
                release_date = ""
            # different keyboards
            try:
                overview = res.overview
            except:
                overview = ""
            try:
                title = res.title
            except:
                title = ""
            try:
                vote_average = res.vote_average
            except:
                vote_average = ""
            try:
                runtime = res.runtime
            except:
                runtime = ""
            keyboard_first = types.InlineKeyboardMarkup()
            keyboard_last = types.InlineKeyboardMarkup()
            keyboard_middle = types.InlineKeyboardMarkup()
            keyboard_single = types.InlineKeyboardMarkup()
            item_tv = types.InlineKeyboardButton(text='🔍 сериал', callback_data="tv " + text + ' 0')
            item_prev = types.InlineKeyboardButton(text='<-', callback_data='movie ' + text + ' ' + str(film_no - 1))
            item = types.InlineKeyboardButton(text='Смотреть', url=url)
            item_next = types.InlineKeyboardButton(text='->', callback_data='movie ' + text + ' ' + str(film_no + 1))
            keyboard_first.add(item_tv, item, item_next)
            keyboard_middle.add(item_prev, item, item_next)
            keyboard_last.add(item_prev, item)
            keyboard_single.add(item_tv, item)
            # checking which keyboard to use
            if (int(len(search)) == 1):
                keyboard = keyboard_single
            elif (film_no == 0):
                keyboard = keyboard_first
            elif (film_no == len(search) - 1):
                keyboard = keyboard_last
            else:
                keyboard = keyboard_middle
            url = base_movie_url + str(res.id)
            if len(overview) > 480:
                overview = overview[0:480] + "..."
            photo_text = "*" + str(title) + "*"
            if vote_average:
                photo_text += "\n\n*Рейтинг:* " + str(res.vote_average)
            if release_date:
                photo_text += "\n\n*Год: *" + release_date
            if genres:
                photo_text += "\n\n*Жанры:* " + genres + "\n\n"
            if runtime:
                photo_text += "*Продолжительность:* " + str(runtime) + " мин.\n\n"
            if overview:
                photo_text += str(overview)
            if res.poster_path:
                photo_url = tmdb_photo_url + res.poster_path

                bot.send_photo(chat_id, photo_url, caption=photo_text, reply_markup=keyboard, parse_mode="Markdown")
            else:
                bot.send_message(chat_id, photo_text, reply_markup=keyboard, parse_mode="Markdown")

    else:
        bot.send_message(chat_id, "Ничего не нашлось")


# tv card
def send_tv_card(message, text, tv_no):
    chat_id = message.chat.id
    tv = TV()
    search = tv.search(text)
    if search:
        res = search[tv_no]
        res = (tv.details(res.id))
        print("\n\n res = ")
        print(res)
        if res:
            tv_id = res.id
            url = base_tv_url + str(tv_id)
            try:
                genres = []
                genres_list = res.genres
                for genre in genres_list:
                    genres.append(genre.name)
                genres = genres[0:4]
                genres = ",".join(genres)
            except:
                genres = ""
                err("genres")
            try:
                release_date = res.first_air_date[0:4] + " - " + res.last_air_date[0:4]
            except:
                release_date = ""
                err("date")
            # different keyboards
            try:
                overview = res.overview
            except:
                overview = ""
                err("overview")
            try:
                title = res.name
            except:
                title = ""
                err("title")
            try:
                vote_average = res.vote_average
            except:
                vote_average = ""
                err("vote_average")
            try:
                runtime = res.episode_run_time[0]
            except:
                runtime = ""
                err("runtime")
            print("\n" + str(title) + ", \n" + str(vote_average) + ", \n" + str(release_date) + ", \n" + \
                  str(genres) + "\n" + str(runtime) + ", \n" + str(overview))
            keyboard_first = types.InlineKeyboardMarkup()
            keyboard_last = types.InlineKeyboardMarkup()
            keyboard_middle: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
            keyboard_single = types.InlineKeyboardMarkup()
            item_tv = types.InlineKeyboardButton(text='🔍 фильм', callback_data="movie " + str(text) + " 0")
            item_prev = types.InlineKeyboardButton(text='<-', callback_data='tv ' + text + ' ' + str(tv_no - 1))
            item = types.InlineKeyboardButton(text='Смотреть', callback_data='seasons ' + tv_id)
            item_next = types.InlineKeyboardButton(text='->', callback_data='tv ' + text + ' ' + str(tv_no + 1))
            keyboard_first.add(item_tv, item, item_next)
            keyboard_middle.add(item_prev, item, item_next)
            keyboard_last.add(item_prev, item)
            keyboard_single.add(item_tv, item)
            print("HERE")
            # checking which keyboard to use
            if (int(len(search)) == 1):
                keyboard = keyboard_single
            elif (tv_no == 0):
                keyboard = keyboard_first
            elif (tv_no == len(search) - 1):
                keyboard = keyboard_last
            else:
                keyboard = keyboard_middle
            url = base_tv_url + str(res.id)
            if len(overview) > 480:
                overview = overview[0:480] + "..."
            photo_text = "*" + str(title) + "*"
            if vote_average:
                photo_text += "\n\n*Рейтинг:* " + str(res.vote_average)
            if release_date:
                photo_text += "\n\n*Год: *" + release_date
            if genres:
                photo_text += "\n\n *Жанры:* " + genres + "\n\n"
            if runtime:
                photo_text += "*Длина серии:* " + str(runtime) + " мин.\n\n"
            if overview:
                photo_text += str(overview)
            if res.poster_path:
                photo_url = tmdb_photo_url + res.poster_path

                bot.send_photo(chat_id, photo_url, caption=photo_text, reply_markup=keyboard, parse_mode="Markdown")
            else:
                bot.send_message(chat_id, photo_text, reply_markup=keyboard, parse_mode="Markdown")

    else:
        item = types.InlineKeyboardButton(text='Искать фильм', callback_data="movie " + text + " 0")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(item)
        bot.send_message(chat_id, "Ничеого не нашлось", reply_markup=keyboard)


# season card
def send_season_card(message, tv_id):
    chat_id = message.chat.id
    tv = TV()
    res = tv.details(tv_id)
    if res:
        try:
            title = str(res.name)
            seasons = res.seasons
            seasons_list = []
            keyboard = types.InlineKeyboardMarkup()
            for index, season in enumerate(seasons):
                season_no = str(index + 1)
                season_no_text = season_no + ' сезон'
                item = types.InlineKeyboardButton(text=season_no_text, callback_data="episodes " + title \
                                                                                     + ' ' + season_no + ' ' + episodes_count + ' ' + tv_id)
                keyboard.add(item)
            bot.send_message(chat_id, "Смотерть " + title, reply_markup=keyboard)
        except:
            err("seasons")


# season card
def send_episode_card(message, title, season_no, episodes_count, tv_id):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    try:
        for episode_no in range(episodes_count-1):
            item = types.InlineKeyboardButton(text="Серия ", url = base_movie_url + tv_id + '-' + season_no + '-' + episode_no)
            keyboard.add(item)
    except:
        err("send episode")



# кнопка /cancel
@bot.message_handler(commands=['start'])
def strat(message):
    bot.send_message(message.chat.id, "Какой фильм ищем?")


# получили название
@bot.message_handler(func=lambda m: True)
def handle_text_photo(message):
    chat_id = message.chat.id
    text = message.text
    movie = Movie()
    search = movie.search(text)
    if search:
        film_no = 0
        send_film_card(message, text, film_no)
    else:
        bot.send_message(chat_id, "Ничего не нашлось")


# Конкретный фильм
@bot.callback_query_handler(func=lambda call: True)
def film_card(call):
    call_data = call.data.split()
    key = call_data[0]
    del call_data[0]
    if key == "movie":
        film_no = int(call_data[-1])
        del call_data[-1]
        text = " ".join(call_data)
        try:
            send_film_card(call.message, text, film_no)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            print("Card Error")
    elif key == "tv":
        tv_no = int(call_data[-1])
        del call_data[-1]
        text = " ".join(call_data)
        try:
            send_tv_card(call.message, text, tv_no)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            print("Card Error")
    elif key == "seasons":
        tv_id = int(call_data[-1])
        del call_data[-1]
        tv_id = call_data[0]
        try:
            send_season_card(call.message, tv_id)
        except:
            print("Season Error")
    elif key == "episodes":  # "episodes " + title + season_no + episodes_count
        tv_id = int(call_data[-1])
        del call_data[-1]
        episodes_count = nt(call_data[-1])
        del call_data[-1]
        season_no = int(call_data[-1])
        del call_data[-1]
        title = " ".join(call_data)
        try:
            send_episode_card(call.message, title, season_no, episodes_count, tv_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            print("Card Error")


if __name__ == "__main__":
    bot.infinity_polling()
