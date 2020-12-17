from datetime import datetime
import spotipy
import spotipy.util as util
import sharp_darwin.exceptions
from collections import defaultdict


class SharpDarwin:
    def __init__(self, username=None, scope=None, credCache=None):
        self.scope = "user-follow-read user-read-playback-state user-top-read playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative"
        if scope:
            self.scope = scope
        self.username = username
        self.token = None
        self.client = None
        self.args = None
        self.credCache = credCache

    def timestamp(self):
        dt = datetime.now()
        return dt.isoformat()

    def artistsFollowed(self, limit=20):
        res = self.client.current_user_followed_artists(limit)

        artists = []

        # defaultdict(int) provides a value of 0 for all new members
        genres = defaultdict(int)

        for artist in res["artists"]["items"]:
            artists.append({
                "name": artist["name"],
                "totalFollowers": artist["followers"]["total"],
                "id": artist["id"],
                "genres": artist["genres"],
                "popularity": artist["popularity"]
            })

            for genre in artist["genres"]:
                genres[genre] += 1

        return {
                "timestamp": self.timestamp(),
                "artists": artists, 
                "genres": genres
        }

    def audioAnalysis(self, trackID):
        res = self.client.audio_analysis(trackID)
        return res

    def deviceList(self):
        res = self.client.devices()
        return res

    def currentPlayback(self):
        res = self.client.current_playback()

        if res is None:
            return None

        if res["context"]:
            context = {"type": res["context"]["type"],
                       "id": res["context"]["uri"].split(":")[-1]}
            context["name"] = self.getPlaylistName(context["id"])

        else:
            context = None

        device = res["device"]

        artists = []
        for artist in res["item"]["album"]["artists"]:
            artists.append({"name": artist["name"], "id": artist["id"]})

        album = {
            "type": res["item"]["album"]["album_type"],
            "id": res["item"]["album"]["id"],
            "name": res["item"]["album"]["name"],
            "release_date": res["item"]["album"]["release_date"],
            "total_tracks": res["item"]["album"]["total_tracks"]
        }

        track = {
            "name": res["item"]["name"],
            "id": res["item"]["id"],
            "popularity": res["item"]["popularity"],
        }

        state = {
            "progress_ms": res["progress_ms"],
            "repeat_state": res["repeat_state"],
            "shuffle_state": res["shuffle_state"],
            "timestamp": res["timestamp"]
        }

        output = {
            "timestamp": self.timestamp(),
            "context": context,
            "device": device,
            "artists": artists,
            "album": album,
            "track": track,
            "state": state
        }

        return output

    def getPlaylistName(self, playlist_id):
        # Get playlist name
        playlistName = None
        try:
            res = self.client.user_playlist(
                user=self.username, playlist_id=playlist_id, fields="name")
            return res["name"]
        except BaseException:
            raise PlaylistNotFound(playlist_id)

    def login(self):
        if not self.token:
            self.token = util.prompt_for_user_token(
                username=self.username, scope=self.scope, 
                cache_path=self.credCache)
        try: 
            if self.token:
                self.client = spotipy.Spotify(auth=self.token)
            else:
                raise noTokenForUsername(self.username)
        except spotipy.client.SpotifyException as e:
            raise exceptions.LoginFailure(e)
        return True

    def me(self):
        return self.client.me()

    def playlistCopy(self, source, target):
        # Counter for total tracks copied
        count = 0

        # Add tracks. This bit is in a sub-funtion to support the
        # 100 track limit of user_playlist_add_tracks
        def addTracks(target, tracks):
            res = self.client.user_playlist_add_tracks(
                user=self.username, playlist_id=target, tracks=tracks)
            # Retun of a snapshot ID == Success
            if "snapshot_id" in res:
                return True
            else:
                raise FailedToCopyPlaylist(res)

        # Get a track list of the source playlist
        tracks = []
        # Limit to 100... user_playlist_add_tracks can only add 100 tracks at a
        # time
        res = self.client.user_playlist_tracks(
            user=self.username, playlist_id=source, limit=100)
        for track in res["items"]:
            # Add tracks to list
            tracks.append(track["track"]["id"])

        try:
            # Actually add the track list to the target playlist
            addTracks(target, tracks)
            # incr the counter
            count = count + len(tracks)
            # reset the tracks list
            tracks = []
        except BaseException:
            raise

        # Pagination, if needed
        while res["next"]:
            res = self.client.next(res)
            for track in res["items"]:
                # Add tracks to list
                tracks.append(track["track"]["id"])

            try:
                # Actually add the track list to the target playlist
                addTracks(target, tracks)
                # incr the counter
                count = count + len(tracks)
                # reset the tracks list
                tracks = []
            except BaseException:
                raise

        # Return results
        return {
            "timestamp": self.timestamp(),
            "source": source, 
            "target": target, 
            "count": count
        }

    def playlistCreate(self, playlistName, public, descr=None):
        # Create the playlist
        res = self.client.user_playlist_create(
            user=self.username,
            name=playlistName,
            public=public)
            #description=descr)

        # Check for success
        if "id" in res:
            # Return an object of data
            return {
                "timestamp": self.timestamp(),
                "Success": True,
                "playlist-id": res["id"],
                "playlist-name": res["name"],
                "description": res["description"],
                "public": res["public"],
                "collaborative": res["collaborative"]}
        else:
            # Raise failure
            raise CreatePlaylistFailure(res)

    def playlistDelete(self, playlist_id):
        res = self.client.user_playlist_unfollow(
            user=self.username, playlist_id=playlist_id)
        if not res:
            return True
        else:
            raise PlaylistDeleteFailed(res)


    def playlistList(self, mine=False):
        # Array of paginated playlist returns
        lists = []
        # Consolidation of pagination
        items = []
        # Final output
        output = []

        # Make initial requet for user's playlists
        playlists = self.client.user_playlists(self.username)
        lists.append(playlists)

        # Pagination
        while playlists["next"]:
            playlists = self.client.next(playlists)
            lists.append(playlists)

        # Consolidate pagination
        for lst in lists:
            for item in lst["items"]:
                items.append(item)

        # Loop though playlists
        for playlist in items:
            # Skip playlists not created by the user
            if mine:
                if playlist["owner"]["id"] != self.username:
                    continue
            # Get the total numer of tracks
            total = int(playlist["tracks"]["total"])
            # Create an object for each playlist
            output.append({
                "owner": playlist["owner"]["id"],
                "id": playlist["id"],
                "total": total,
                "playlistName": playlist["name"]
            })
        # Done!
        return {
            "timestamp": self.timestamp(),
            "count": len(output), 
            "data": output
        }

    def topArtists(self, limit, time_range):
        try:
            res = self.client.current_user_top_artists(
                limit=limit, time_range=time_range)
        except BaseException:
            raise

        artists = []

        # defaultdict(int) provides a value of 0 for all new members
        genresDict = defaultdict(int)

        for artist in res["items"]:
            artists.append({
                "name": artist["name"],
                "genres": artist["genres"], 
                "popularity": artist["popularity"],
                "url": artist["external_urls"]["spotify"]
            })

            for genre in artist["genres"]:
                genresDict[genre] += 1


        genres = [ {"genre": x, "count": genresDict[x]} for x in genresDict ]

        output = {"artists": artists, "genres": genres}
        return {
            "timestamp": self.timestamp(),
            "count": len(artists),
            "time_range": time_range,
            "data": output}

    def topTracks(self, limit, time_range):
        try:
            res = self.client.current_user_top_tracks(
                limit=limit, time_range=time_range)
        except BaseException:
            raise

        tracks = []

        for track in res["items"]:
            artists = []
            for artist in track["artists"]:
                artists.append(artist["name"])
            tracks.append({
                "uri":  track["uri"],
                "url": track["external_urls"]["spotify"],
                "trackName": track["name"],
                "popularity": track["popularity"],
                "artists": artists,
                "trackID": track["id"],
                "releaseDate": track["album"]["release_date"],
                "albumName": track["album"]["name"]
            }
            )

        output = {"tracks": tracks}
        return {
            "timestamp": self.timestamp(),
            "count": len(tracks),
            "time_range": time_range,
            "data": output}

    def trackList(self, playlist_id):
        # Get playlist name
        playlistName = self.getPlaylistName(playlist_id)

        tracks = []

        # Get initial track list
        res = self.client.user_playlist_tracks(
            user=self.username, playlist_id=playlist_id)
        for track in res["items"]:
            tracks.append(track["track"]["id"])

        # Paginate
        while res["next"]:
            res = self.client.next(res)
            for track in res["items"]:
                tracks.append(track["track"]["id"])

        # object containing final count and data
        output = {
            "timestamp": self.timestamp(),
            "count": len(tracks),
            "playlistName": playlistName,
            "playlist_id": playlist_id,
            "tracks": []}

        # Parse the track data
        trackData = []
        for item in res["items"]:
            track = item["track"]
            artists = []

            href = track["href"]
            albumName = track["name"]
            trackName = track["name"]
            trackID = track["id"]
            popularity = track["popularity"]
            addedAt = item["added_at"]

            for a in track["artists"]:
                artists.append(a["name"])

            trackData.append({
                "artists": artists,
                "albumName": albumName,
                "trackName": trackName,
                "popularity": popularity,
                "trackID": trackID,
                "addedAt": addedAt,
                "href": href
            })
        # Add track data to the final results
        output["tracks"] = trackData
        return output

    def tracksAdd(self, playlist_id, trackID):
        # Add track to playlist
        if trackID is True:
            trackInfo = self.currentPlayback()
            trackID = trackInfo["track"]["id"]

        self.addTrackToPlaylist(playlist_id, [trackID])
        return True

    def addTrackToPlaylist(self, playlist_id, tracks):
        # Add one (str) or more (list) tracks to a playlist
        res = self.client.user_playlist_add_tracks(
            user=self.username, playlist_id=playlist_id, tracks=tracks)
        # Retun of a snapshot ID == Success
        if "snapshot_id" in res:
            return True
        else:
            raise FailedToAddToPlaylist

    def newReleases(self, country, limit=50, next=None):
        data = []
        res = self.client.new_releases(country=country, limit=limit)
        data.append(res)
        
        while res["albums"]["next"]:
            res = self.next(res["albums"])
            data.append(res)
        return data
        
    def next(self, url):
        return self.client.next(url)

