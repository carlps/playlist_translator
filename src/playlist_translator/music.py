"""
Define music related objects here like Playlist, Song, etc.
"""
from dataclasses import dataclass
from typing import List

# TODO figure out circular dependencies
# maybe just define this in services
from .services import Service


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
    service: Service
    songs: List[Song]
