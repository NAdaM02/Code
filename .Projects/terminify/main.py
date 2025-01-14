import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id='67c0740055b9412da3e1e14978c42742',
        client_secret='4116025cf230497699d6feb972d8bfc7',
        redirect_uri='http://localhost',
        ),
    )

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

"""if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])"""


artist = spotify.artist(urn)
print(artist)

user = spotify.user('plamere')
print(user)
