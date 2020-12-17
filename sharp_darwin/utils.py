import json
from os.path import abspath
import argparse

# Various random things which are useful


def jsonPrint(data):
    """ Pretty print json data """
    print(
        json.dumps(
            data,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )


def writeJSONFile(filename, data, pretty=False):
    """ Write json data to file """
    fqpn = abspath(filename)
    with open(fqpn, "w") as f:
        if pretty:
            json.dump(
                data,
                f,
                sort_keys=True,
                indent=4,
                separators=(
                    ',',
                    ': '))
        else:
            json.dump(data, f)


def argParser():
    parser = argparse.ArgumentParser(description="Spotify Playlist Manager")
    subparsers = parser.add_subparsers(
        help='Command help',
        dest="command")
        #required=True)

    ###############
    # Global args #
    ###############
    parser.add_argument(
        "--json",
        action="store_true",
        help="Display output as json")

    parser.add_argument(
        "--env",
        type=str,
        default="./.env",
        help="Location of dot env file (default: ./.env)")

    ################
    # Sub-commands #
    ################

    """ artists followed """
    sp_cmd_artists_followed = subparsers.add_parser(
        "artists-followed", help="Listing of artists followed")
    sp_cmd_artists_followed.add_argument(
        "--limit", type=int, default=20, help="List limit (default: 20)")

    """" audio analysis """
    sp_cmd_audio_analysis = subparsers.add_parser(
        "audio-analysis", help="Audio analysis for a track")
    sp_cmd_audio_analysis.add_argument(
        "--id", type=str, nargs=1, required=True, help="Track ID")

    """ current playback """
    sp_cmd_current_playback = subparsers.add_parser(
        "current-playback", help="Show the current playback")

    """ device List """
    sp_cmd_device_list = subparsers.add_parser(
        "device-list", help="List devices")

    """ me """
    sp_cmd_me = subparsers.add_parser("me", help="Show user info")

    """ playlist-copy """
    sp_cmd_playlist_copy = subparsers.add_parser(
        "playlist-copy", help="Copy tracks from source to target")
    sp_cmd_playlist_copy.add_argument(
        "--source", type=str,
        nargs=1, required=True,
        help="Source playlist ID from which to copy tracks")
    sp_cmd_playlist_copy.add_argument(
        "--target", type=str,
        nargs=1, required=True,
        help="Target playlist ID to copy tracks to")

    """ playlist-create """
    sp_cmd_playlist_create = subparsers.add_parser(
        "playlist-create", help="Create playlists")
    sp_cmd_playlist_create.add_argument(
        "--name",
        type=str,
        nargs=1,
        required=True,
        help="Playlist Name")
    sp_cmd_playlist_create.add_argument(
        "--public",
        action="store_true",
        help="Make playlist public")
    sp_cmd_playlist_create.add_argument(
        "--descr", type=str, nargs=1, help="Optional description")

    """ playlist-delete """
    sp_cmd_playlist_delete = subparsers.add_parser(
        "playlist-delete", help="Delete playlists")
    sp_cmd_playlist_delete.add_argument(
        "--id",
        type=str,
        nargs=1,
        required=True,
        help="ID of playlist")
    sp_cmd_playlist_delete.add_argument(
        "--confirm",
        action="store_true",
        required=True,
        help="Confirm this list will be deleted")

    """ playlist-list """
    sp_cmd_playlist_show = subparsers.add_parser(
        "playlist-list", help="Lists playlists")
    sp_cmd_playlist_show.add_argument(
        "--mine",
        action="store_true",
        default=False,
        help="Shows only my playlists")

    """ top-artists """
    sp_cmd_top_artists = subparsers.add_parser(
        "top-artists", help="Show user's top artists")
    sp_cmd_top_artists.add_argument(
        "--limit", type=int,
        default=50,
        help="Number of results to return (default/max: 50)")
    sp_cmd_top_artists.add_argument(
        "--time", choices=["short", "med", "long"],
        default="long",
        help="Choose timeframe [short, med, long] (default: long)")

    """ top-tracks """
    sp_cmd_top_tracks = subparsers.add_parser(
        "top-tracks", help="Show user's top tracks")
    sp_cmd_top_tracks.add_argument(
        "--limit", type=int,
        default=50,
        help="Number of results to return (default/max: 50)")
    sp_cmd_top_tracks.add_argument(
        "--time", choices=["short", "med", "long"],
        default="long",
        help="Choose timeframe [short, med, long] (default: long)")

    """ tracks-list """
    sp_cmd_tracks_list = subparsers.add_parser(
        "tracks-list", help="List tracks in a playlist")
    sp_cmd_tracks_list.add_argument(
        "--id",
        type=str,
        nargs=1,
        required=True,
        help="Playlist ID")

    """ tracks-add """
    sp_cmd_tracks_list = subparsers.add_parser(
        "tracks-add", help="Adds a track to a playlist")
    sp_cmd_tracks_list.add_argument(
        "--playlist-id",
        required=True,
        type=str, nargs=1,
        help="Playlist ID")
    mutex = sp_cmd_tracks_list.add_mutually_exclusive_group(required=True)
    mutex.add_argument(
        "--id",
        type=str,
        nargs=1,
        help="Track ID")
    mutex.add_argument(
        "--now",
        action="store_true",
        help="Add the current song")

    """ new-releases """
    sp_cmd_new_releases = subparsers.add_parser(
        "new-releases", help="Lists new releases"
    )
    sp_cmd_new_releases.add_argument(
        "-c", "--country", default="US", type=str,
        help="An ISO 3166-1 alpha-2 country code"
    )

    return parser
