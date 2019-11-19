from dataclasses import dataclass, field

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator

APPLE = 'Apple'
GOOGLE = 'Google'
SERVICES = (APPLE, GOOGLE)


@dataclass
class Config:
    # TODO Services
    from_service: str = field(init=False)
    to_service: str = field(init=False)
    plalist_id: str = field(init=False)

    # class level constants
    APPLE = "APPLE"
    GOOGLE = "GOOGLE"
    SERVICES = (APPLE, GOOGLE)
    FROM = "FROM"
    TO = "TO"

    def get_input(self):
        """
        Gets input and sets class attributes
        """
        self.get_from_service()
        self.get_to_service()
        self.get_playlist_id()
        self.get_from_service_api_key()
        self.get_to_service_api_key()

    def get_from_service(self):
        direction = self.FROM
        self.from_service = self._get_service(direction)

    def get_to_service(self):
        direction = self.TO
        self.to_service = self._get_service(direction)

    def _get_service(self, direction):
        """

        """
        validator = self.validator
        available_services = self.available_services
        service_completer = WordCompleter(available_services, ignore_case=True)
        service_message = f"{direction} service {available_services}: "
        service = prompt(service_message,
                         completer=service_completer,
                         validator=validator,
                         validate_while_typing=False,
                         )
        service = service.title()
        return service

    @property
    def available_services(self):
        """
        This is to make sure we don't config from and to as the same services.
        If no services have been set, then all services are available.
        If from_service has been set, then all other services are available.
        If to_service has been set, then this shouldn't be called as both
        services are already set.
        """
        if hasattr(self, 'from_service'):
            return tuple(service for service in self.SERVICES
                         if service != self.from_service)
        else:
            return self.SERVICES

    @property
    def validator(self):
        """
        """
        def service_is_valid(service):
            return service.title() in self.available_services

        error_message = f"Service must be one of: {self.available_services}"
        validator = Validator.from_callable(service_is_valid,
                                            error_message=error_message,
                                            move_cursor_to_end=True)
        return validator

    def get_playlist_id(self):
        # TODO what kind of validation can we do?
        self.playlist_id = prompt("Playlist ID: ")


def playlist_translator():
    config = Config()
    config.get_input()
