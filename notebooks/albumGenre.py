from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json
import os

url = "https://album.giacomonanni.info/"

req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "html.parser")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

albumIDs = []

for link in links:
    a, b = link.find('album/'), link.find('?si=')
    albumID = link[a+6:b]
    albumIDs.append(albumID)

cid = os.environ['SPOTIFY_API_KEY']
secret = os.environ['SPOTIFY_API_SECRET']
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager 
                     =client_credentials_manager)

print(sp)


dictionary = {}

for albumID in albumIDs:
    try:
        album = sp.album(albumID)
        artistID = album['artists'][0]['id']
        artist = sp.artist(artistID)

        print("genres:", artist['genres'])

        for i in artist['genres']:
            if i not in dictionary:
                dictionary[i] = [ albumID]
            else:
                 dictionary[i].append(albumID)
            
        time.sleep(.5)
    except:
        continue


out = open('data.json', 'w') 
r = json.dumps(dictionary, indent=4)
out.write(r)
out.close()