#!/usr/bin/env python3

from sys import exit
from sharp_darwin.frontend import *
from sharp_darwin.utils import argParser
import argcomplete

def main():
    ###########################
    # Setup                   #
    ###########################
    # Load up the cli args
    parser = argParser()

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    
    sharpDarwin = init(args)
    sharpDarwin.args = args

    ###########################
    # Commands                #
    ###########################
    if args.command == "artists-followed":
        # Listing of artists followed
        artistsFollowed(sharpDarwin)

    elif args.command == "audio-analysis":
        # Audio analysis for a specified track
        audioAnalysis(sharpDarwin)

    elif args.command == "current-playback":
        # Current playback
        currentPlayback(sharpDarwin)

    elif args.command == "device-list":
        deviceList(sharpDarwin)

    elif args.command == "me":
        # Return Spotify account info
        me(sharpDarwin)

    elif args.command == "playlist-copy":
        # Copy a playlist to another
        playlistCopy(sharpDarwin)

    elif args.command == "playlist-create":
        # Create a playlist
        playlistCreate(sharpDarwin)

    elif args.command == "playlist-delete":
        # Delete a playlist
        playlistDelete(sharpDarwin)

    elif args.command == "playlist-list":
        # Get a curated listing of playlists
        playlistList(sharpDarwin)

    elif args.command == "top-artists":
        # Get user's top artists
        topArtists(sharpDarwin)

    elif args.command == "top-tracks":
        # Get user's top tracks
        topTracks(sharpDarwin)

    elif args.command == "tracks-list":
        # List tracks in a playlist
        tracksList(sharpDarwin)

    elif args.command == "tracks-add":
        # Add track to playlist
        tracksAdd(sharpDarwin)

    elif args.command == "new-releases":
        # List new releases
        newReleases(sharpDarwin)

    else:
        # This should never happen... unless I made a mistake.
        parser.print_help()
        print("\nUnexpected command? Given: ", args.command)


if __name__ == "__main__":
    main()
