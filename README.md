# Sharp-Darwin
Python CLI Spotify utility.

## Why?
Why "sharp-darwin"? Why not? Naming things can be difficult so why not pick two words, glue them together, and call it done?

## Purpose
This project started with a need to consolidate my Spotify playlists. I keep monthly playlists of the things I like. After three years of Spotify monthly playlist making... I have a lot of playlists. My goal was to consolidate the lists into quarterly (most recent lists), half year, and year playlists (oldest lists).

## Getting Started
1. Install sharp-darwin from PyPi: https://pypi.org/project/sharp-darwin/ ```pip install sharp-darwin```
2. Next, you'll need to set up your own Spotify app: https://developer.spotify.com/my-applications
3. Create a new app, or reuse an existing. If creating a new app, provide at least the required fields.. whatever you want. After creation, click *Edit Settings*. In the *Redirect URIs* field, simply enter `https://localhost`.
4. On the main app page, you'll need to fetch the *Client ID* and *Client Secret*.
5. Set up envionmental vars as indicated in the below section.
6. Run the app! ```sharp-darwin --help```.

## Environmental Variables
Sharp-Darwin can import configuration from envionmental variables or from a .env file. If you choose to use a .env file, you can specifiy the location of the file on the command line ```sharp-darwin --env /path/to/my/dot/env```.
### Variables
Most items should be self-explanatory. Here's a few which are not:
* SPOTIPY_REDIRECT_URI: set this to ```https://localhost``` to locallly fetch an OAuth token. If you know what you're doing, you know how to set this. Otherwise.. stick to the suggested.
* SHARP_DARWIN_CRED_CACHE: this is the location of the Spotipy OAuth credential cache. It will default to the current working directoy if not set.

Example ```.env``` file:
```
SPOTIPY_USERNAME=you_spotify_username
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=https://localhost
SHARP_DARWIN_CRED_CACHE=/path/to/cred/cache
```

## Auto-complete
Sharp-Darwin supports bash completion via https://github.com/kislyuk/argcomplete. Follow the install instructions for ```argcomplete```. After installing, you can do ```eval "$(register-python-argcomplete sharp-darwin)"```.
