# spotify_controller
<p align = "center">
  <img width="400" alt="spotify_controller window" src="https://github.com/user-attachments/assets/02a16265-74bf-4f56-86eb-054c6be9f58c" />
  <br>
  <em>The Spotify controller</em>
</p>

I wanted to make a way to control my Spotify when I don't always have access to my phone for extended periods of time, without running Spotify in my web browser

## Overview
I explored HTTP requests and HTTP servers to access certain commands in the Spotify Web API. There was no use of the spotipy library.

## Features
- HTTPServer made in Python
- Usage of HTTP requests
- Can pause, play, skip, add to queue, play one of your playlists, ![Uploading Screenshot 2026-11-09 19.44.12.png…]()
and get the current song
- Shows a window that:
  - Displays the current song title with the album cover that refreshes every 5 seconds
  - Displays the next 7 songs in the queue that refreshes every 5 seconds
  - Has button options explained in Usage

## Technologies
- Python
- Spotify Web API

## Installation
1. Clone the repository and enter the folder:
  ```
  git clone https://github.com/SETHCODES13/spotify_controller.git
  cd spotify_controller
  ```
2. Create and activate a virtual environment(optional but recommended):

  **Linux & macOS**
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  ```
  
  **Windows(Command Prompt)**
  ```
  python -m venv .venv
  .venv\Scripts\activate
  ```
3. Install the required Libraries:
  ```
  pip install -r requirements.txt
  ```

***Note***: `sudo apt install python3-tk` on Debian or Ubuntu if Tkinter is missing

## Setup
1. Create an app on the [Spotify Developer API](https://developer.spotify.com/)
2. Add the redirect URL `http://127.0.0.1:8888/callback`
3. Paste your Client ID in the `client_id` line in `heard_em_say.py`

## Usage
<p align = "center">
  <img width="400" alt="spotify_controller window" src="https://github.com/user-attachments/assets/175830b4-8e2c-4ddf-bee5-bae8a7c3daf9" />
  <br>
  <em>The standard look of the window</em>
</p>
<p align = "center">
  <img width="400" alt="spotify_controller window" src="https://github.com/user-attachments/assets/1c61b57b-bcf5-4438-90df-88af2cb1dc2f" />
  <br>
  <em>Adding something to the queue</em>
</p>

When you run `python3 heard_em_say.py`, it shows the pop-up window shown above, which will be fully activated when a song is playing
| Button | Function |
| :------ | :------- |
| `Add to Queue` | Adds the song entered in the textbox in the format (Song Name - Song Artist) |
| `Pause/Play` | Pauses and plays the song based on whether it's paused or not. 
|              |*Spotify API deactivates the player shortly after being paused, so resuming can fail*|
| `Next Song` | Plays the next song|
| `Previous Song` | Plays the previous song |
| `Play Playlist` | Plays the playlist selected in the dropdown menu |
| `Shuffle` | Choose whether the playlist is going to be on shuffle |
| `Repeat` | Choose whether the playlist is going to repeat itself |


## License
MIT License, see [LICENSE](LICENSE.txt)
