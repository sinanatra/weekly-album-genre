from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json

url = "https://spotify-top.com/user/sinanatra"

req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "html.parser")

links = []
for link in soup.findAll('a'):
    try:
        if "https://open.spotify.com/artist" in link.attrs["href"]:
            links.append(link.attrs["href"].split("/")[-1])
    except:
        continue

cid = os.environ['SPOTIFY_API_KEY']
secret = os.environ['SPOTIFY_API_SECRET']
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

print(sp)

dictionary = {}

for id in links:
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


out = open('./scr/assets/data.json', 'w') 
r = json.dumps(dictionary, indent=4)
out.write(r)
out.close()