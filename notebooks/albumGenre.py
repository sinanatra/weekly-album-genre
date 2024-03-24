from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json

#url = "https://spotify-top.com/user/sinanatra"
url = "https://musicalyst.com/user/sinanatra"

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

# take data from the json
script_tag = soup.find('script', id='__NEXT_DATA__')
script_content = script_tag.string
data = json.loads(script_content)
page_props_data = data['props']['pageProps']['data']['artists']['short']

for link in page_props_data:
    links.append(link['id'])

#print(len(links))

cid = os.environ['SPOTIFY_API_KEY']
secret = os.environ['SPOTIFY_API_SECRET']

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

dictionary = {}

for id in list(set(links)):
    try:
        artist = sp.artist(id)
        #print("genres:", artist['genres'])
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
