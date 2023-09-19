from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

CLIENT_ID = YOUR_CLIENT_ID
CLIENT_SECRET = YOUR_CLIENT_SECRET
REDIRECT_URI = "http://example.com"
URL = "https://www.billboard.com/charts/hot-100/"
song_uri =[]

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
year = date.split("-")[0]
response = requests.get(f"{URL}{date}")
web = response.text
soup = BeautifulSoup(web, "html.parser")
all_songs = soup.find_all(name="h3", id="title-of-a-story")
song_list = [song.getText().strip() for song in all_songs][6:-16:4]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# Searching Spotify for songs by title
for song in song_list:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
play_list = sp.user_playlist_create(user=user_id,
                                    name=f"{date} Billboard 100",
                                    public=False,
                                    )

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=play_list["id"], items=song_uri)
