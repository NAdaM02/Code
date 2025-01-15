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

numbers = (
(".o.", "| |", "'0'"),
(".~1", "  |", "  |"),
("˛=,", " ,I", "2__"),
("˙´\\", " ~3", ".˛/"),
("/  ", "4+*", " |"),
("_~~", "5o.", "--/ "),
("˛o. ", "6*.", "˙o˙"),
("\"\"7", " / ", "*  "),
(",o,", ",8, ", "˙o˙"),
(".o,", "´~9", " / ")
)

print("\n\n\n")

next = ("×.", "-|>", "×˙")
pause = ("O O", "O O", "O O")
resume = ("×.", "O|>", "×˙")
previous = (" .×", "<|-", " ˙×")
like = (",-.-,", "', ,'", "  `  ")
liked = (",=_=,", "\%X%/", " ˇ÷ˇ ")

print()
print("\n".join(like))
print()
print("\n".join(liked))
print()
print("\n".join(pause))
print()
print("\n".join(resume))
