from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import pywhatkit
from pytube import YouTube


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET");

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8");
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8");
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers, data= data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token;

token = get_token()


def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search/"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("Nothing")
        return None
    
    return json_result

def get_songs_from_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100&offset=0"
    headers = get_auth_header(token)
    res = get(url, headers=headers)
    json_res = json.loads(res.content)
    return json_res['items']

def get_songs_by_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    response = get(url, headers=headers)
    json_res = json.loads(response.content)["tracks"]
    return json_res

result = search_for_artist(token, "arijit")
artist_id = result["artists"]["items"][0]["id"]

# songs = get_songs_by_id(token, artist_id)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1 }. {song['name']}")

playlist = get_songs_from_playlist(token , "0xeRK2QFKxIXXo7J81fjSe")

size = len(playlist)

songs_list = []
url_list = []

for idx in range(1, size):
    songs_list.append(playlist[idx]['track']['name'])

print('playlist done')

for x in songs_list:
    y = pywhatkit.playonyt(x, open_video=False)
    url = get(y).url
    url_list.append(url)

print('urls done')

for i in range(0, size):
    yt= YouTube(url_list[i])

    video = yt.streams.filter(only_audio=True).first()

    destination = '/songs/'
    out_file = video.download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)



