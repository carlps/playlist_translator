"""
Define music related objects here like Playlist, Song, etc.
"""
from dataclasses import dataclass
import datetime
from typing import Optional

from . import parsers


@dataclass
class Artist:
    """
    """
    name: str


@dataclass
class Song:
    """
    """
    song_id: str
    name: str
    artist: Artist
    release_date: datetime.date
    album_name: str
    track_number: int
    composer_name: Optional[str]

    @property
    def artist_track(self):
        return ' '.join([self.artist.name, self.name])