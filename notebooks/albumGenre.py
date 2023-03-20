from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json

# cid = os.environ['SPOTIFY_API_KEY']
# secret = os.environ['SPOTIFY_API_SECRET']

cid = "d4303311201249bb8372a3ecfeb4643e"
secret = "492a6986a5924c7c9b75ff272aa02626"
redirect = "http://www.giacomonanni.info/"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

from spotipy.oauth2 import SpotifyOAuth
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect,scope=scope))

links = []


results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])



dictionary = {}

for id in list(set(links)):
    try:
        artist = sp.artist(id)

        print("genres:", artist['genres'])

        for i in artist['genres']:
            if i not in dictionary:
                dictionary[i] = [ id]
            else:
                 dictionary[i].append(id)
            
        time.sleep(.5)
    except:
        continue


out = open('data.json', 'w') 
r = json.dumps(dictionary, indent=4)
out.write(r)
out.close()