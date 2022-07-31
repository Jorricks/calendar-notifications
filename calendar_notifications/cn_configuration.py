from __future__ import annotations

import getpass
import logging
import subprocess
from pathlib import Path

from calendar_notifications.handle_event_start.abstract_event_start_handler import AbstractEventStartHandler
from calendar_notifications.handle_event_start.zoom_meeting_handler import ZoomMeetingHandler

from mac_notifications.singleton import Singleton

logger = logging.getLogger(__name__)


class CNConfiguration(metaclass=Singleton):
    def __init__(
        self,
        private_ical_url: str = None,
        path_to_ical_result_cache: Path | None = None,
        event_start_handler: AbstractEventStartHandler | None = None,
    ):
        self.private_ical_url: str = private_ical_url or self.get_item_from_keyvault("ical.google.com")
        self.ical_result_cache_path = path_to_ical_result_cache or Path.home() / "calendar_notifications" / "ical.cache"
        self.event_start_handler = event_start_handler or ZoomMeetingHandler

    @staticmethod
    def get_item_from_keyvault(service: str, key_name: str | None = None) -> str:
        """
        This uses the mac keyvault to get your private iCalendar link. If it is not there, it will ask you to set it.
        This is the most secure way to store your iCalendar :).
        """
        key_name = key_name or f"{service}-password"
        username = getpass.getuser()
        command = f"security find-generic-password -a {username} -s {service} -l {key_name} -w"
        try:
            output = subprocess.run(
                command, universal_newlines=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            ).stdout.strip()
        except subprocess.CalledProcessError as exception:
            logger.info(f"Got the following {exception=}.")
            return CNConfiguration.input_password_for_keyvault(service=service, key_name=key_name)
        return output

    @staticmethod
    def input_password_for_keyvault(service: str, key_name: str) -> str:
        password = input(f"Please put the password for {service=}:")
        CNConfiguration.set_item_in_keyvault(service=service, password=password, key_name=key_name)
        return password

    @staticmethod
    def set_item_in_keyvault(service: str, password: str, key_name: str | None = None) -> None:
        key_name = key_name or f"{service}-password"
        username = getpass.getuser()
        command = f'security add-generic-password -a {username} -s {service} -l {key_name} -w "{password}"'
        subprocess.run(command, check=True, shell=True)
