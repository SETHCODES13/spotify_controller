import requests
import time

global heard_em_say_uri
global wake_up_mr_west_uri

#returns track uri, length in milliseconds of the currently playing song, how far you are into the currently playing song, and the image url
def get_currently_playing(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if r.status_code == 204:
        print("Nothing is playing")
        return None
    elif r.status_code == 429:
        print("Rate limited. Retry after", r.headers.get("Retry-After"), "seconds")
        return None
    elif r.status_code != 200:
        print(r.status_code, " ", r.text)
        return None

    song = r.json()['item']
    if song is None:
        print(r.status_code, " ", r.text)
        return
    else:
        return r.json()['item']['uri'], r.json()['item']['duration_ms'], r.json()['progress_ms'], r.json()["item"]["album"]["images"][0]["url"], r.json()['item']['name'], r.json()['item']['artists'][0]['name']
 
#Adds a song you choose to the queue
def add_to_queue(access_token, audio_uri):
    headers = {"Authorization": f"Bearer {access_token}"}
    verif = {"uri": audio_uri}

    r = requests.post("https://api.spotify.com/v1/me/player/queue", headers=headers, params=verif)
    if r.status_code == 200 or r.status_code == 204:
        print("Added to queue")
    else:
        print(r.status_code, " ", r.text)
    time.sleep(0.3)

#Returns song uri after searching by name and artist
def find_song(access_token, song_name, artist_name=None):
    headers = {"Authorization": f"Bearer {access_token}"}

    if artist_name:
        query = f"track:{song_name} artist:{artist_name}"
    else:
        query = f"track:{song_name}"

    params = {"q": query, "type": "track", "market": "US", "limit": 10}

    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if r.status_code != 200:
        print("Search failed:", r.status_code)
        return None

    tracks = r.json()["tracks"]["items"]

    for track in tracks:
        if track.get("name").lower() == song_name.lower():
            print("Song found")
            return track["uri"]

    return None

#Returns device_id
def get_device_code(access_token):
    headers = {"Authorization":f"Bearer {access_token}"}

    r = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)

    devices = r.json()["devices"]
    for device in devices:
        if device['type'].lower() == 'smartphone':
            print("Device found")
            return device['id']

#Pauses the current song
def pause_song(access_token, device_id):
    headers = {"Authorization":f"Bearer {access_token}"}
    payload = {"device_id":device_id}
    r = requests.put("https://api.spotify.com/v1/me/player/pause", headers=headers, params=payload)
    if r.status_code == 204 or r.status_code == 200:
        print("Song paused")
    else:
        print(r.status_code, " ", r.text)

#Plays the next song
def skip_song(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.post("https://api.spotify.com/v1/me/player/next", headers=headers)
    
    if r.status_code in [200,204]:
        print("Song skipped")
    else:
        print(r.status_code, " ", r.text)

#Plays the previous song
def previous_song(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.post("https://api.spotify.com/v1/me/player/previous", headers=headers)
    
    if r.status_code in [200,204]:
        print("Previous Song Playing")
    else:
        print(r.status_code, " ", r.text)

#Unpauses and plays the current song
def resume_song(access_token, context_uri=None, device_id=None):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"device_id": device_id} if device_id else {}
    json = {"uris": [context_uri]} if context_uri else{}
    
    r = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, params=params, json=json)
    
    if r.status_code in [200, 204]:
        print("Song resumed")
    else:
        print(f"Error {r.status_code}: {r.text}")

#returns a dictionary of the queue songs formatted {"song_name":"artist_name"} 
def list_next_queue(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    r = requests.get("https://api.spotify.com/v1/me/player/queue", headers=headers)

    if r.status_code not in[200,204]:
        if r.status_code == 429:
            print("Rate limited. Retry after", r.headers.get("Retry-After"), "seconds")
        return {}

    queue_songs = r.json()['queue']

    queue = {}

    for track in queue_songs:
        queue[track["name"]] = track["artists"][0]["name"]

    return queue

#Returns image url
def get_image_url(access_token, current_song):
    headers = {"Authorization": f"Bearer {access_token}"}
    track_id = current_song.split(":")[2]
    r = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    if r.status_code == 200:
        images = r.json()["album"]["images"]
        if images:
            return images[0]["url"]
    if r.status_code == 429:
        print("Rate limited. Retry after", r.headers.get("Retry-After"), "seconds")
    else:
        print(r.status_code, " ", r.text)
    return None 

#returns dictionary of all users playlists in format{"name":"playlist_uri"}
def get_user_playlists(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    
    playlists = {}

    if r.status_code == 200:
        items = r.json()['items']
        for item in items:
            playlists[item['name']] = item['uri']
    else:
        print(r.status_code, " ", r.text)
        return playlists
    
    print("Playlists found")
    return playlists
