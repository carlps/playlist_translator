"""
Define music related objects here like Playlist, Song, etc.
"""
from dataclasses import dataclass
import datetime
from typing import List, Optional, Type, TypeVar

from glom import glom

from . import services

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
    service_id: str
    name: str
    artist: Artist
    url: Optional[str]
    release_date: datetime.date
    album_name: str
    track_number: int
    composer_name: str

    @classmethod
    def from_apple_track(cls: Type[S], track: dict) -> S:
        if track['type'] != 'songs':
            raise AttributeError("Unsupported track type")

        track_attrs = track['attributes']
        artist = Artist(track_attrs['artistName'])
        release_date = datetime.datetime.strptime(track_attrs['releaseDate'],
                                                  services.Apple.dt_format
                                                  ).date()

        return cls(
            service_id=track['id'],
            name=track_attrs['name'],
            artist=artist,
            url=track_attrs['url'],
            release_date=release_date,
            album_name=track_attrs['albumName'],
            track_number=track_attrs['trackNumber'],
            composer_name=track_attrs['composerName'],
        )

    @classmethod
    def from_gplay_entry(cls: Type[S], entry: dict) -> S:

        track = entry['track']
        artist = Artist(track['artist'])
        # gplay only has realease year for a song
        release_date = datetime.date(year=track['year'], month=1, day=1)

        return cls(
            service_id=entry['trackId'],
            name=track['title'],
            artist=artist,
            url=None,  # gplay has no song url # TODO see if we can delete from apple
            release_date=release_date,
            album_name=track['album'],
            track_number=track['trackNumber'],
            composer_name=track['composer']
        )


@dataclass
class Playlist:
    """
    """
    # TODO maybe i don't need service -- or maybe an instantiated service?
    service: Type[services.Service]
    songs: List[Song]

    @classmethod
    def from_apple_response(cls: Type[P], apple_response: dict) -> P:
        tracks_list = glom(apple_response, services.Apple.tracks_glom)
        # returns a list of lists for some reason? TODO figure it out
        assert len(tracks_list) <= 1
        songs = [Song.from_apple_track(track) for track in tracks_list[0]]
        return cls(services.Apple, songs)

    @classmethod
    def from_gplay_response(cls: Type[P], gplay_response: List) -> P:
        songs = [Song.from_gplay_entry(entry) for entry in gplay_response]
        return cls(services.GooglePlay, songs)
