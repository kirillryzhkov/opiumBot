import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import bot_tokens

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=bot_tokens.client_id,
    client_secret=bot_tokens.client_secret
))

def get_top_tracks():
    try:
        playlist_id = "6qv7CRaZr9nJaamM8Xtrv6"
        results = sp.playlist_items(playlist_id, limit=10)
        return [{"name": t["track"]["name"], "artist": t["track"]["artists"][0]["name"], "url": t["track"]["external_urls"]["spotify"]} for t in results["items"]]
    except Exception as e:
        print(f"Ошибка получения топ-10 треков: {e}")
        return None

def get_playlists_by_genre(genre):
    try:
        results = sp.category_playlists(category_id=genre, limit=10)
        return [{"name": p["name"], "url": p["external_urls"]["spotify"]} for p in results["playlists"]["items"]]
    except Exception as e:
        print(f"Ошибка получения плейлистов жанра {genre}: {e}")
        return []

def get_random_tracks_by_genre(genre):
    try:
        results = sp.search(q=f"genre:{genre}", type="track", limit=50)
        if results["tracks"]["items"]:
            tracks = random.sample(results["tracks"]["items"], min(len(results["tracks"]["items"]), 10))
            return [{"name": t["name"], "artist": t["artists"][0]["name"], "url": t["external_urls"]["spotify"]} for t in tracks]
        return []
    except Exception as e:
        print(f"Ошибка получения случайных треков жанра {genre}: {e}")
        return []

def search_tracks(query):
    try:
        results = sp.search(q=query, type="track", limit=5)
        return [{"name": t["name"], "artist": t["artists"][0]["name"], "url": t["external_urls"]["spotify"]} for t in results["tracks"]["items"]]
    except Exception as e:
        print(f"Ошибка поиска треков: {e}")
        return None

def search_playlists(query):
    try:
        results = sp.search(q=query, type="playlist", limit=5)
        return [{"name": p["name"], "url": p["external_urls"]["spotify"]} for p in results["playlists"]["items"]]
    except Exception as e:
        print(f"Ошибка поиска плейлистов: {e}")
        return None
