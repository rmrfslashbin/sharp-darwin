import os
from pathlib import Path
from sharp_darwin.SharpDarwin import SharpDarwin
from dotenv import load_dotenv
from sharp_darwin.utils import jsonPrint


def init(args):
    # Ensure python can support f-strings
    try:
        xyz = eval('f""')
    except SyntaxError:
        print(
            "This app uses Python f-strings. Please upgrade to or run using Python >= 3.6")
        exit(1)
    except BaseException:
        raise

    #  Dotenv env loader
    env_path = Path(args.env).resolve()
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)

    # Get the username from env
    if "SPOTIPY_USERNAME" not in os.environ:
        print("Missing envionment variable 'SPOTIPY_USERNAME'")
        print(
            "Add your username to the .env file or export SPOTIPY_USERNAME='your-username'")
        exit(1)

    username = os.environ["SPOTIPY_USERNAME"]


    credCache = None
    if "SHARP_DARWIN_CRED_CACHE" in os.environ:
        credCache = os.environ["SHARP_DARWIN_CRED_CACHE"]

    # Used for calls out to spotify
    sharpDarwin = SharpDarwin(username=username, credCache=credCache)

    # Log onto Spotify
    try:
        sharpDarwin.login()
    except BaseException:
        raise

    return sharpDarwin


def artistsFollowed(sharpDarwin):
    res = sharpDarwin.artistsFollowed(sharpDarwin.args.limit)
    jsonPrint(res)


def audioAnalysis(sharpDarwin):
    res = sharpDarwin.audioAnalysis(sharpDarwin.args.id[0])
    jsonPrint(res)


def currentPlayback(sharpDarwin):
    res = sharpDarwin.currentPlayback()
    # jsonPrint(res)

    if res is None:
        if sharpDarwin.args.json:
            jsonPrint({"success": False,
                       "message": "nothing is currently playing"})
        else:
            print("Nothing currently playing")
    else:
        if sharpDarwin.args.json:
            jsonPrint(res)
        else:
            track = [
                {"Name": res["track"]["name"]},
                {"Popularity": res["track"]["popularity"]},
                {"ID": res["track"]["id"]}
            ]

            album = [
                {"Name": res["album"]["name"]},
                {"Release Date": res["album"]["release_date"]},
                {"ID": res["album"]["id"]}
            ]

            artists = []
            for artist in res["artists"]:
                artists.append(artist["name"])

            playlist = None
            if res["context"]:
                playlistName = res["context"]["name"]
                playlistID = res["context"]["id"]
                playlist = [
                    {"Playlist Name": playlistName},
                    {"Playlist ID": playlistID}
                ]

            device = [
                {"Device Name": res["device"]["name"]},
                {"Device Type": res["device"]["type"]},
                {"Volume": res["device"]["volume_percent"]},
                {"Device ID": res["device"]["id"]}
            ]
            from datetime import datetime
            state = [
                {"Progress (ms)": res["state"]["progress_ms"]},
                {"Repeat": res["state"]["repeat_state"]},
                {"Suffle": res["state"]["shuffle_state"]},
                {"Timestamp": datetime.fromtimestamp(res["state"]["timestamp"] / 1000).isoformat()}
            ]

            labelWidth = 13

            print()
            print("Track info")
            print("==========")
            print(f"    {'Artists':{labelWidth}s} : {', '.join(artists)}")
            for i in track:
                for x, y in i.items():
                    print(f"    {x:{labelWidth}s} : {y}")

            print()
            print("Album info")
            print("==========")
            for i in album:
                for x, y in i.items():
                    print(f"    {x:{labelWidth}s} : {y}")

            print()
            print("Playlist")
            print("========")
            if not playlist:
                print("    (no playlist)")
            else:
                for i in playlist:
                    for x, y in i.items():
                        print(f"    {x:{labelWidth}s} : {y}")

            print()
            print("Device Info")
            print("==========")
            for i in device:
                for x, y in i.items():
                    print(f"    {x:{labelWidth}s} : {y}")

            print()
            print("State Info")
            print("==========")
            for i in state:
                for x, y in i.items():
                    print(f"    {x:{labelWidth}s} : {y}")


def deviceList(sharpDarwin):
    res = sharpDarwin.deviceList()
    jsonPrint(res)


def me(sharpDarwin):
    """ Show basic user data """
    ret = sharpDarwin.me()
    if sharpDarwin.args.json:
        jsonPrint(ret)
    else:
        displayName = ret["display_name"]
        followers = ret["followers"]["total"]
        href = ret["href"]
        userID = ret["id"]
        userType = ret["type"]
        uri = ret["uri"]
        print(f"{'Display Name':12s}: {displayName}")
        print(f"{'Followers':12s}: {followers}")
        print(f"{'href':12s}: {href}")
        print(f"{'User ID':12s}: {userID}")
        print(f"{'User Type':12s}: {userType}")
        print(f"{'URI':12s}: {uri}")


def playlistCopy(sharpDarwin):
    """ Copy a playlist to another """
    source = sharpDarwin.args.source[0]
    target = sharpDarwin.args.target[0]

    try:
        jsonPrint(sharpDarwin.playlistCopy(source=source, target=target))
    except BaseException:
        raise


def playlistCreate(sharpDarwin):
    """ Create a playlist """
    playlistName = sharpDarwin.args.name[0]
    public = False
    descr = ""

    if sharpDarwin.args.public:
        public = True

    if sharpDarwin.args.descr:
        descr = sharpDarwin.args.descr[0]

    # Create the playlist
    try:
        jsonPrint(
            sharpDarwin.playlistCreate(
                playlistName=playlistName,
                public=public,
                descr=descr
            )
        )
    except BaseException:
        raise


def playlistDelete(sharpDarwin):
    """ Delete a playlist """
    try:
        sharpDarwin.playlistDelete(sharpDarwin.args.id[0])
        if sharpDarwin.args.json:
            jsonPrint({"success": True})
        else:
            print("Playlist deleted")
    except BaseException:
        raise


def playlistList(sharpDarwin):
    """ Display playlists """
    data = sharpDarwin.playlistList(mine=sharpDarwin.args.mine)

    if sharpDarwin.args.json:
        jsonPrint(data)
    else:
        # Get the longest char len
        # to format the output correctly
        longest = 0
        for playlist in data["data"]:
            charLength = len(playlist["owner"])
            if charLength > longest:
                longest = charLength

        # Output header
        print(f"{'id':^22s} | {'owner':^{longest}s} | {'total':^4s} | name")
        # Display data
        for playlist in data["data"]:
            total = int(playlist["total"])
            print(
                f"{playlist['id']} | {playlist['owner']:{longest}s} | {total:>5d} | {playlist['playlistName']}")


def topArtists(sharpDarwin):
    """ Show top artist details for the user """
    if sharpDarwin.args.time == "short":
        time_range = "short_term"
    if sharpDarwin.args.time == "med":
        time_range = "medium_term"
    if sharpDarwin.args.time == "long":
        time_range = "long_term"

    res = sharpDarwin.topArtists(
        limit=sharpDarwin.args.limit,
        time_range=time_range)
    if sharpDarwin.args.json:
        jsonPrint(res)
    else:
        count = res["count"]
        time_range = res["time_range"]
        artists = res["data"]["artists"]
        genres = sorted(
            res["data"]["genres"],
            reverse=True,
            key=lambda x: x["count"])

        longestArtist = 0
        for artist in artists:
            artistName = len(artist["name"])
            if artistName > longestArtist:
                longestArtist = artistName

        itemCount = 0
        print("\n===Artists===\n")
        print(f"rank | {'artists':^{longestArtist}s} | genres")
        for artist in artists:
            itemCount = itemCount + 1
            artistName = artist["name"]
            artistGenres = artist["genres"]
            print(
                f"#{itemCount:3d} | {artistName:{longestArtist}s} | {', '.join(artistGenres)}")

        print("\n===Genres===\n")
        longestGenre = 0
        for genre in genres:
            if len(genre["genre"]) > longestGenre:
                longestGenre = len(genre["genre"])
        print(f"{'genre':^{longestGenre}s} | occurrences")
        for genre in genres:
            print(f"{genre['genre']:{longestGenre}s} | {genre['count']}")


def topTracks(sharpDarwin):
    """ Show top artist details for the user """
    if sharpDarwin.args.time == "short":
        time_range = "short_term"
    if sharpDarwin.args.time == "med":
        time_range = "medium_term"
    if sharpDarwin.args.time == "long":
        time_range = "long_term"

    res = sharpDarwin.topTracks(
        limit=sharpDarwin.args.limit,
        time_range=time_range)

    if sharpDarwin.args.json:
        jsonPrint(res)
    else:
        longestTrack = 0
        longestAlbum = 0
        longestArtist = 0
        for track in res["data"]["tracks"]:
            trackName = len(track["trackName"])
            albumName = len(track["albumName"])
            artists = len(", ".join(track["artists"]))

            if trackName > longestTrack:
                longestTrack = trackName
            if albumName > longestAlbum:
                longestAlbum = albumName
            if artists > longestArtist:
                longestArtist = artists

        print(f"{'track':^{longestTrack}s} | {'album':^{longestAlbum}s} | {'artists':^{longestArtist}s} | {'release date':^12s} | {'popularity':^10s} | {'track ID':^22s}")
        for track in res["data"]["tracks"]:
            releaseDate = "------------"
            if track["releaseDate"]:
                releaseDate = track["releaseDate"]
            print(f"{track['trackName']:{longestTrack}s} | {track['albumName']:{longestAlbum}s} | {', '.join(track['artists']):{longestArtist}s} | {releaseDate:12s} | {track['popularity']:<10d} | {track['trackID']}")


def tracksList(sharpDarwin):
    """ List tracks in a playlist """
    playlist_id = sharpDarwin.args.id[0]
    res = sharpDarwin.trackList(playlist_id)

    if sharpDarwin.args.json:
        jsonPrint(res)
    else:

        # Get max field widths
        longestArtist = 0
        longestAlbum = 0
        longestAddedAtDate = 0
        longestTrackName = 0
        for track in res["tracks"]:
            artists = len(", ".join(track["artists"]))
            album = len(track["albumName"])
            trackName = len(track["trackName"])

            if artists > longestArtist:
                longestArtist = artists
            if album > longestAlbum:
                longestAlbum = album
            if trackName > longestTrackName:
                longestTrackName = trackName

        print(f"{'artists':^{longestArtist}s} | {'album':^{longestAlbum}s} | {'track name':^{longestTrackName}s} | {'date added':^20s} | {'popularity':^10s} | {'track ID':^22s}")
        for track in res["tracks"]:
            addedAt = "------------"
            if track["addedAt"]:
                addedAt = track["addedAt"]

            print(f"{', '.join(track['artists']):{longestArtist}s} | {track['albumName']:{longestAlbum}s} | {track['trackName']:{longestTrackName}s} | {addedAt:20s} | {track['popularity']:<10d} | {track['trackID']}")


def tracksAdd(sharpDarwin):
    if sharpDarwin.args.now:
        tid = True
    else:
        tid = sharpDarwin.args.id[0]
    jsonPrint(sharpDarwin.tracksAdd(sharpDarwin.args.playlist_id[0], tid))


def newReleases(sharpDarwin):
    data = sharpDarwin.newReleases(country=sharpDarwin.args.country)
    if sharpDarwin.args.json:
        jsonPrint(data)
    else:
        for s in data:
            for item in s["albums"]["items"]:
                artists = [artist["name"] for artist in item["artists"]]                
                print(item["name"])
                print(f"  Artists:      {', '.join(artists)}")
                print(f"  Type:         {item['album_type']}")
                print(f"  Release Date: {item['release_date']}")
                print(f"  Total Tracks: {item['total_tracks']}")
                print(f"  Spotify ID:   {item['id']}")
                print()
            
        
    
