# spotify_controller
I wanted to make Wake Up Mr West and Heard 'Em Say by Kanye always play in order.

## Overview
I explored HTTP requests and HTTP servers to access certain commands in the Spotify Web API. There was no use of the spotipy library.

## Features
- HTTPServer made in Python
- Usage of HTTP requests
- Can pause, play, skip, add to queue, and get the current song
- Detects Heard 'Em Say and Wake Up Mr West from active listening device

## Technologies
- Python
- Spotify Web API

## Installation
- Use `git clone https://github.com/SETHCODES13/spotify_controller.git`
- Needs Python libraries: `pip install requests readchar`

## Setup
I made an app using the Spotify Web API. I then used OAuth2 Authorization to get an access token with this callback that you need to use as well unless you modify that section of the code: `http://127.0.0.1:8888/callback`. This was used to make HTTP requests to the Spotify Web API. You will need to put in your own client id as mine is there currently. Playback control requires Spotify Premium. After the first run, it will open a browser where you allow the permissions necessary to run this. You do not need a `homecoming.tcd` file to run this code

## Usage
When you run `heard_em_say.py` it will tell you when it is ready to receive commands by printing `"Enter your command"`. It will print this every time it is ready
| Command | Function |
| :------ | :------- |
| `c` | Prints the current song playing |
| `n` | Allows you to enter the title and artist, then adds that song to the queue |
| `p` | Pauses the current song |
| `s` | Skips the current song |
| `r` | Resumes the current song (currently not perfect) |
| `q` | Quits the program and shuts down the server |

## License
MIT License, see [LICENSE](LICENSE.txt)
