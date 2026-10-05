from urllib.request import Request, urlopen
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json

#url = "https://spotify-top.com/user/sinanatra"
#url = "https://musicalyst.com/user/sinanatra"
url = "https://api.stats.fm/api/v1/users/sinanatra/top/artists?range="

links = []
# weeks = last 4 weeks, months = last 6 months, lifetime = all time
for time_range in ["weeks", "months", "lifetime"]:
    req = Request(url + time_range, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    data = json.loads(urlopen(req).read())

    for item in data['items']:
        # an artist can have several spotify ids, use the first
        ids = item['artist']['externalIds'].get('spotify', [])
        if ids:
            links.append(ids[0])

# stop here and keep the old data.json if the profile came back empty
if not links:
    raise SystemExit("No artists found at %s. Is the profile still public?" % url)

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

# every spotify lookup failed (bad keys?): keep the old data.json
if not dictionary:
    raise SystemExit("No genres found. Are the Spotify keys still valid?")


out = open('data.json', 'w') 
r = json.dumps(dictionary, indent=4)
out.write(r)
out.close()
