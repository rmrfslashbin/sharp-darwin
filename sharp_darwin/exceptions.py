class LoginFailure(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class noTokenForUsername(Exception):
    def __init__(self, username):
        self.username = username
        Exception.__init__(self, f"Can't login as user ({self.username})")


class CreatePlaylistFailure(Exception):
    def __init__(self, results):
        Exception.__init__(self, results)


class PlaylistDeleteFailed(Exception):
    def __init__(self, results):
        Exception.__init__(self, results)


class FailedToCopyPlaylist(Exception):
    def __init__(self, results):
        Exception.__init__(self, results)


class PlaylistNotFound(Exception):
    def __init__(self, playlist_id):
        Exception.__init__(self, playlist_id)


class FailedToAddToPlaylist(Exception):
    def __init__(self, results):
        Exception.__init__(self, results)
