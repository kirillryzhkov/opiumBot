from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers import start, top_tracks, popular_playlists, show_playlists, random_tracks_by_genre, handle_search, favorites
from db import init_db
import logging
import bot_tokens

TOKEN = bot_tokens.TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    init_db()
    app = Application.builder().token(TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", handle_search))

    # Обработчики текстовых сообщений
    app.add_handler(MessageHandler(filters.Text("Топ-10 треков недели"), top_tracks))
    app.add_handler(MessageHandler(filters.Text("Популярные плейлисты"), popular_playlists))
    app.add_handler(MessageHandler(filters.Text("Случайные треки по жанру"), random_tracks_by_genre))
    app.add_handler(MessageHandler(filters.Text("Избранное"), favorites))

    # Обработчики callback-запросов
    app.add_handler(CallbackQueryHandler(show_playlists, pattern="genre_"))
    app.add_handler(CallbackQueryHandler(random_tracks_by_genre, pattern="track_genre_"))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
