import requests
import secrets
import string
import hashlib
import base64
import webbrowser
from typing import Final
from through_the_wire import MyHTTPServer, server_handler, run
import threading
import we_major
import time
from pathlib import Path
import customtkinter as ctk
from io import BytesIO
from PIL import Image

def generate_code_verifier(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


global refresh_token
has_token = False
is_paused = False

STATE: Final = generate_code_verifier(32)
code_verifier = generate_code_verifier(64)
code_verifier_bytes = code_verifier.encode('utf-8')
hashed_code_verifier = hashlib.sha256(code_verifier_bytes)
code_challenge = base64.urlsafe_b64encode(hashed_code_verifier.digest()).decode('utf-8')
code_challenge = code_challenge.rstrip('=')

client_id = "08a41d35326f478f8d7dfaefb01dde35"
redirect_uri = "http://127.0.0.1:8888/callback"
auth_URL = "https://accounts.spotify.com/authorize"

verif = {'client_id':client_id, 'response_type':'code', 'redirect_uri':redirect_uri, 'scope': 'user-read-currently-playing user-read-playback-state user-modify-playback-state', 'code_challenge_method':'S256', 'code_challenge':code_challenge, 'state':STATE}
auth_url = requests.Request('GET', auth_URL, params=verif).prepare().url

file_path = Path("homecoming.tcd")

if file_path.is_file() and file_path.stat().st_size > 0:
    # Already authorized: refresh the access token
    with open(file_path, "r") as file:
        refresh_token = file.read().strip()

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data=payload
    )

else:
    # First authorization: run your existing browser + callback process
    httpd = MyHTTPServer(('', 8888), server_handler, STATE)

    t = threading.Thread(target=run, args=(httpd,))
    t.start()

    webbrowser.open_new(auth_url)

    httpd.my_event.wait()
    httpd.shutdown()
    t.join()

    if httpd.auth_error is not None:
        print("Authorization failed")
        exit()

    payload = {
        "grant_type": "authorization_code",
        "code": httpd.authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": code_verifier
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data=payload
    )

    refresh_token = response.json().get("refresh_token")

    with open(file_path, "w") as file:
        file.write(refresh_token)

access_token = response.json().get("access_token")

print("Access Token Acquired")
print()

try:
    with open("homecoming.tcd","w") as file:
        file.write(refresh_token)
        file.close()
except FileNotFoundError:
    print("Error: File not found")

device_code = we_major.get_device_code(access_token)
running = True
auto_switch = False
paused_song = None
current_song = we_major.get_currently_playing(access_token)[0]

print()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class SpotifyControllerScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("spotify_controller")
        self.geometry("500x650")
        self.resizable(True, True)

        self.after_id = None

        self.song_info = None

        self.queue_frame = ctk.CTkFrame(self, width=200, height=210)
        self.queue_frame.pack(side = "right", fill="y", padx=15, pady=20)

        self.queue_box = ctk.CTkTextbox(self.queue_frame, width=180, height=580)
        self.queue_box.pack(padx=10, pady=10)

        self.add_queue_btn = ctk.CTkButton(self, text="Add To Queue", command=self.add_queue, fg_color="#333333")
        self.add_queue_btn.pack(pady=5, padx=20, fill="x")

        self.play_btn = ctk.CTkButton(self, text="Pause / Play", command=self.toggle_play)
        self.play_btn.pack(pady=5, padx=20, fill="x")

        self.skip_btn = ctk.CTkButton(self, text="Next Song", command=self.next_song, fg_color="#333333")
        self.skip_btn.pack(pady=5, padx=20, fill="x")

        self.previous_btn = ctk.CTkButton(self, text="Previous Song", command=self.previous_song)
        self.previous_btn.pack(pady=5, padx=20, fill="x")

        self.input_entry = ctk.CTkEntry(master=self, width=200, height=5 ,corner_radius=4 ,placeholder_text="Enter song for queue",font=("Helvetica", 14),text_color="#FFFFFF",fg_color="#2b2b2b")
        self.input_entry.pack(pady=5)

        self.current_song_frame = ctk.CTkFrame(self, width=200, height = 100)
        self.current_song_frame.pack(pady=10, padx=20, fill="x")
        
        self.current_song_textbox = ctk.CTkTextbox(self.current_song_frame, width=180, height=100)
        self.current_song_textbox.pack(padx=10, pady=10)

        self.cover_image = None
        self.last_cover_url = None
        self.cover_label = ctk.CTkLabel(self, text="")
        self.cover_label.pack(pady=10)

        self.refresh_all()



    def toggle_play(self):
        global is_paused
        if is_paused:
            is_paused = False
            we_major.resume_song(access_token)
        else:
            is_paused = True
            we_major.pause_song(access_token, device_code)

    def next_song(self):
        we_major.skip_song(access_token)
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = self.after(1000, self.refresh_all)

    def previous_song(self):
        we_major.previous_song(access_token)
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = self.after(1000, self.refresh_all)

    def add_queue(self):
        song_string = self.input_entry.get()
        song_string_array = song_string.rsplit(" - ",1)
        if len(song_string_array) != 2:
            return
        song_name = song_string_array[0].strip()
        song_artist = song_string_array[1].strip()
        audio_uri = we_major.find_song(access_token, song_name, song_artist)
        we_major.add_to_queue(access_token,audio_uri)
        self.after(1000, self.fill_queue_box)

    def fill_queue_box(self):
        self.queue_box.configure(state="normal")
        self.queue_box.delete("1.0", "end")
        queue = we_major.list_next_queue(access_token)
        for name, artist in queue.items():
            string = f"{name} - {artist}\n"
            self.queue_box.insert("end", string)
        self.queue_box.configure(state="disabled")

    def fill_current_song_textbox(self):
        self.current_song_textbox.configure(state="normal")
        self.current_song_textbox.delete("1.0", "end")
        current_song_info = self.song_info
        string = f"{current_song_info[4]} -\n{current_song_info[5]}"
        if string is None:
            self.current_song_textbox.insert("end", "Nothing is playing")
        else:
            self.current_song_textbox.insert("end", string)
        self.current_song_textbox.configure(state="disabled")

    def update_cover(self):
        current_song_info = self.song_info
        if current_song_info is None:
            return
        else:
            current_song = current_song_info[0]
            song_length = (current_song_info[1] - current_song_info[2]) + 1000
            url = current_song_info[3]
            if current_song is not None:
                if url is not None and url != self.last_cover_url:
                    response = requests.get(url)
                    image = Image.open(BytesIO(response.content))
                    self.cover_image = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
                    self.cover_label.configure(image=self.cover_image)
                    self.last_cover_url = url

    def refresh_all(self):
        self.song_info = we_major.get_currently_playing(access_token)
        song_length = 10000

        if self.song_info is not None:
            #call the update methods
            self.fill_current_song_textbox()
            self.update_cover()
            self.fill_queue_box()
            song_length = (self.song_info[1] - self.song_info[2]) + 1000

        self.after_id = self.after(min(song_length,30000), self.refresh_all)

if __name__ == "__main__":
    window = SpotifyControllerScreen()
    window.mainloop()
        
