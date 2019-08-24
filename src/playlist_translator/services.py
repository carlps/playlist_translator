"""
Define music services in here. All should inherit from Service.
"""
from dataclasses import dataclass


@dataclass
class Service:
    name: str
    base_url: str
    api_key: str = None


@dataclass
class Apple(Service):
    name: str = "Apple"
    base_url: str = "TODO"


@dataclass
class GooglePlay(Service):
    name: str = "Google Play"
    base_url: str = "TODO"
