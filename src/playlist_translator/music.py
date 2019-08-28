"""
Define music related objects here like Playlist, Song, etc.
"""
from dataclasses import dataclass
from typing import List

from . import services


@dataclass
class Artist:
    """
    """
    name: str


@dataclass
class Song:
    """
    """
    name: str
    artist: Artist


@dataclass
class Playlist:
    """
    """
    # TODO maybe i don't need service
    service: 'services.Service'
    songs: List[Song]
