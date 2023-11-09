from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Senthil MovieBot! Please use /getstory command followed by the movie name to get the movie story.")

def get_story_command(update: Update, context: CallbackContext) -> None:
    movie_title = " ".join(context.args)
    movie_story = retrieve_movie_story(movie_title)
    if movie_story:
        update.message.reply_text(f"The story of {movie_title}:\n{movie_story}")
    else:
        update.message.reply_text("Movie not found or an error occurred.")

def retrieve_movie_story(movie_title):
    base_url = "https://api.themoviedb.org/3"
    endpoint = "/search/movie"
    api_key = "fbb140a68ef9c5799994a0bbba539705"

    response = requests.get(
        f"{base_url}{endpoint}?api_key={api_key}&query={movie_title}"
    )

    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            movie_id = results[0]["id"]

            movie_response = requests.get(
                f"{base_url}/movie/{movie_id}?api_key={api_key}"
            )

            if movie_response.status_code == 200:
                movie_data = movie_response.json()
                movie_story = movie_data["overview"]
                return movie_story

    return None

def main() -> None:
    updater = Updater("5953801619:AAFiuKR20mCcCW9xvSJ1Pidk1nAHsi_ape4", use_context = True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("getstory", get_story_command))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


