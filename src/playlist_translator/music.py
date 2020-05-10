"""
Define music related objects here like Playlist, Song, etc.
"""
from dataclasses import dataclass
import datetime
from typing import Dict, List, Optional, Type, TypeVar

from . import parsers

S = TypeVar('S', bound='Song')
P = TypeVar('P', bound='Playlist')


@dataclass
class Artist:
    """
    """
    name: str


@dataclass
class Song:
    """
    """
    # TODO - are these all needed? anything else needed?
    song_id: str
    service_name: str
    name: str
    artist: Artist
    release_date: datetime.date
    album_name: str
    track_number: int
    composer_name: Optional[str]

    @classmethod
    def from_apple_track(cls: Type[S], track: dict) -> S:
        if track['type'] != 'songs':
            raise AttributeError("Unsupported track type")

        track_attrs = track['attributes']
        artist = Artist(track_attrs['artistName'])
        release_date = parsers.parse_apple_date(track_attrs['releaseDate'])

        return cls(
            song_id=track['id'],
            service_name='Apple',
            name=track_attrs['name'],
            artist=artist,
            release_date=release_date,
            album_name=track_attrs['albumName'],
            track_number=track_attrs['trackNumber'],
            composer_name=track_attrs.get('composerName'),
        )

    @classmethod
    def from_gplay_entry(cls: Type[S], entry: Dict) -> S:

        track = entry['track']
        artist = Artist(track['artist'])
        # gplay only has realease year for a song
        release_date = datetime.date(year=track['year'], month=1, day=1)

        return cls(
            song_id=entry['id'],
            service_name='GPlay',
            name=track['title'],
            artist=artist,
            release_date=release_date,
            album_name=track['album'],
            track_number=track['trackNumber'],
            composer_name=track['composer'] or None
        )

    @property
    def artist_track(self):
        return ' '.join([self.artist.name, self.name])


@dataclass
class Playlist:
    songs: List[Song]

    @classmethod
    def from_apple_tracks_list(cls: Type[P], tracks_list: List) -> P:
        songs = [Song.from_apple_track(track) for track in tracks_list]
        return cls(songs)

    @classmethod
    def from_gplay_response(cls: Type[P], gplay_response: List) -> P:
        songs = [Song.from_gplay_entry(entry) for entry in gplay_response]
        return cls(songs)
