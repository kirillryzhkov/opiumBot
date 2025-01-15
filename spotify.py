import base64
import requests
import random
import bot_tokens

# URL для авторизации и API
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

# Функция для получения токена
def get_access_token():
    # Функция для получения токена (копия из шага 3)
    auth_string = f"{"f814986eaf0c4a26a48e8c4c0b486f0c"}:{"110eee39e3c342e797bfcfa7ee2a953f"}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()
    headers = {"Authorization": f"Basic {auth_base64}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token") if response.status_code == 200 else None

def get_top_tracks():
    access_token = get_access_token()
    if not access_token:
        print("Ошибка: токен не получен.")
        return []

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.spotify.com/v1/playlists/6qv7CRaZr9nJaamM8Xtrv6"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [
            {"name": t["track"]["name"], "artist": t["track"]["artists"][0]["name"], "url": t["track"]["external_urls"]["spotify"]}
            for t in data["tracks"]["items"]
        ]
    else:
        print(f"Ошибка: {response.status_code}, {response.json()}")
        return []

# Общая функция для выполнения GET-запросов
def make_get_request(endpoint, params=None):
    access_token = get_access_token()
    
    if not access_token:
        print("Ошибка: токен не получен.")
        return None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка запроса к Spotify API: {response.status_code}, {response.text}")
        return None



def get_playlists_by_genre(genre):
    try:
        endpoint = f"recommendations/available-genre-seeds"
        
        results = make_get_request(endpoint)

        # if results and "playlists" in results:
        #     return [
        #         {"name": p["name"], "url": p["external_urls"]["spotify"]}
        #         for p in results["playlists"]["items"]
        #     ]
        return [results]
    except Exception as e:
        print(f"Ошибка получения плейлистов жанра {genre}: {e}")
        return []


# Получить случайные треки по жанру
def get_random_tracks_by_genre(genre):
    try:
        endpoint = "search"
        params = {"q": f"genre:{genre}", "type": "track", "limit": 50}
        results = make_get_request(endpoint, params)

        if results and results["tracks"]["items"]:
            tracks = random.sample(results["tracks"]["items"], min(len(results["tracks"]["items"]), 10))
            return [
                {
                    "name": t["name"],
                    "artist": t["artists"][0]["name"],
                    "url": t["external_urls"]["spotify"]
                }
                for t in tracks
            ]
        return []
    except Exception as e:
        print(f"Ошибка получения случайных треков жанра {genre}: {e}")
        return []

# Поиск треков
def search_tracks(query):
    try:
        endpoint = "search"
        params = {"q": query, "type": "track", "limit": 5}
        results = make_get_request(endpoint, params)

        if results and results["tracks"]["items"]:
            return [
                {
                    "name": t["name"],
                    "artist": t["artists"][0]["name"],
                    "url": t["external_urls"]["spotify"]
                }
                for t in results["tracks"]["items"]
            ]
        return []
    except Exception as e:
        print(f"Ошибка поиска треков: {e}")
        return None

# Поиск плейлистов
def search_playlists(query):
    try:
        endpoint = "search"
        params = {"q": query, "type": "playlist", "limit": 5}
        results = make_get_request(endpoint, params)

        if results and results["playlists"]["items"]:
            return [
                {
                    "name": p["name"],
                    "url": p["external_urls"]["spotify"]
                }
                for p in results["playlists"]["items"]
            ]
        return []
    except Exception as e:
        print(f"Ошибка поиска плейлистов: {e}")
        return None
