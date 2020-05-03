from dataclasses import dataclass, field
from typing import Dict

from .services import Service, NotAuthenticatedError
from .music import Song, Playlist

@dataclass
class Translator:
    """
    Takes a Playlist and creates new Playlists from those.
    """
    from_service: Service
    playlist: Playlist
    errors: Dict[Song, str] = field(default_factory=dict)

    def to(self, service: Service) -> Playlist:
        # handle if playlist is already to service, just return it back
        if isinstance(service, type(self.from_service)):
            return self.playlist
        
        if not service.is_authenticated:
            raise NotAuthenticatedError("To service must be authenticated")

        new_songs = []

        for song in self.playlist.songs:
            new_song, error = service.lookup_song(song)
            if new_song:
                new_songs.append(new_song)
            if error:
                self.errors[song] = error

        new_playlist = Playlist(new_songs)
        return new_playlist

