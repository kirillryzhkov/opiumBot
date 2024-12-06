from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from spotify import get_top_tracks, search_tracks, search_playlists, get_playlists_by_genre, get_random_tracks_by_genre
from db import save_user, save_query
import logging


logger = logging.getLogger(__name__)

# Главное меню
MAIN_MENU = ReplyKeyboardMarkup(
    [["Топ-10 треков недели", "Популярные плейлисты"],
     ["Случайные треки по жанру", "Избранное"]],
    resize_keyboard=True
)

GENRE_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Pop", callback_data="genre_pop")],
        [InlineKeyboardButton("Rock", callback_data="genre_rock")],
        [InlineKeyboardButton("Hip-Hop", callback_data="genre_hip-hop")],
        [InlineKeyboardButton("Jazz", callback_data="genre_jazz")],
        [InlineKeyboardButton("Electronic", callback_data="genre_electronic")],
    ]
)

async def start(update: Update, context):
    user = update.message.from_user
    save_user(user.id, user.username, user.first_name, user.last_name)
    logger.info(f"Пользователь {user.username} ({user.id}) запустил бота.")

    await update.message.reply_text("Привет! Выберите опцию из меню:", reply_markup=MAIN_MENU)

async def top_tracks(update: Update, context):
    tracks = get_top_tracks()
    if tracks:
        message = "\n".join([f"{t['name']} - {t['artist']} [Слушать]({t['url']})" for t in tracks])
        await update.message.reply_text(f"Топ-10 треков:\n{message}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Не удалось загрузить треки.")

async def popular_playlists(update: Update, context):
    await update.message.reply_text("Выберите жанр для получения популярных плейлистов:", reply_markup=GENRE_KEYBOARD)

async def show_playlists(update: Update, context):
    query = update.callback_query
    await query.answer()
    genre = query.data.split("_")[1]
    playlists = get_playlists_by_genre(genre)
    if playlists:
        message = "\n".join([f"{p['name']} - [Слушать]({p['url']})" for p in playlists])
        await query.edit_message_text(f"Популярные плейлисты ({genre.capitalize()}):\n{message}", parse_mode="Markdown")
    else:
        await query.edit_message_text(f"Не удалось найти плейлисты для жанра {genre.capitalize()}.")

async def random_tracks_by_genre(update: Update, context):
    query = update.callback_query
    if query is None or "genre_" not in query.data:
        await update.message.reply_text("Ошибка: некорректный запрос.")
        return

    await query.answer()
    genre = query.data.split("_")[1]

    tracks = get_random_tracks_by_genre(genre)
    if tracks:
        message = "\n".join([f"{track['name']} - {track['artist']} [Слушать]({track['url']})" for track in tracks])
        await query.edit_message_text(f"Случайные треки для жанра {genre.capitalize()}:\n{message}", parse_mode="Markdown")
    else:
        await query.edit_message_text(f"Не удалось найти треки для жанра {genre.capitalize()}.")

async def handle_search(update: Update, context):
    query = " ".join(context.args)
    
    user = update.message.from_user
    save_query(user.id, query)
    logger.info(f"Пользователь {user.username} ({user.id}) сделал запрос: {query}")

    if not query:
        await update.message.reply_text("Введите запрос для поиска трека или плейлиста.")
        return

    tracks = search_tracks(query)
    if tracks:
        message = "\n".join([f"{t['name']} by {t['artist']} - [Слушать]({t['url']})" for t in tracks])
        await update.message.reply_text(f"Результаты поиска треков:\n{message}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Треки не найдены. Пытаемся найти плейлист.")

    playlists = search_playlists(query)
    if playlists:
        message = "\n".join([f"{p['name']} - [Слушать]({p['url']})" for p in playlists])
        await update.message.reply_text(f"Результаты поиска плейлистов:\n{message}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Плейлисты не найдены.")

async def favorites(update: Update, context):
    await update.message.reply_text("Функция в разработке.")
