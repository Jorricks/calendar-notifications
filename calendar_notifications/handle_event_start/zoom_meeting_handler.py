from __future__ import annotations

import logging
import re
import subprocess
from functools import partial
from pathlib import Path
from typing import Any, Dict

from ical_library.base_classes.component import Component as iCalComponent
from ical_library.ical_components import VEvent, VToDo

from calendar_notifications.handle_event_start.abstract_event_start_handler import AbstractEventStartHandler

from mac_notifications import client

logger = logging.getLogger(__name__)


def get_sources_root() -> Path:
    return Path(__file__).parent.parent.resolve()


def open_zoom_link(conf_number: int | str) -> None:
    """Joins the Zoom meeting specified in your calendar notification."""
    subprocess.run(f'open "zoommtg://adyen.zoom.us/join?action=join&confno={conf_number}&browser=chrome"', shell=True)
    logger.info("Opened zoom into the meeting.")


class ZoomMeetingHandler(AbstractEventStartHandler):
    @staticmethod
    def play_notification_sound(_: iCalComponent):
        path_to_notification = get_sources_root() / "bin" / "notification.mp3"
        subprocess.run(f"afplay {str(path_to_notification.resolve())}", shell=True)
        logger.info("Played notification sound.")

    @staticmethod
    def create_notification_on_mac(ical_instance: iCalComponent) -> None:
        if not isinstance(ical_instance, (VEvent, VToDo)):
            raise ValueError("Should be a VEvent")

        event: VEvent = ical_instance
        extras: Dict[str, Any] = {}
        zoom_meeting_search = re.search(r"adyen\.zoom\.us/j/(\d+)", event.description.value)
        zoom_conf_number = zoom_meeting_search.group(1) if zoom_meeting_search else None
        if zoom_conf_number:
            extras["action_button_str"] = "Join zoom meeting"
            extras["action_callback"] = partial(open_zoom_link, conf_number=zoom_conf_number)
            extras["icon"] = get_sources_root() / "bin" / "zoom.png"
        elif isinstance(ical_instance, VToDo):
            extras["icon"] = get_sources_root() / "bin" / "reminder.png"
        client.create_notification(
            title="Meeting starts now!" if isinstance(ical_instance, VEvent) else "Time for your ToDo!",
            subtitle=event.summary.value,
            **extras,
        )
        logger.info("Created notification :)")

    @staticmethod
    def extra_operation(ical_instance: iCalComponent) -> None:
        """Open the zoom screen and put focus on it :)."""
        subprocess.run("open -a zoom.us.app", shell=True)
        logger.info("Opened zoom.")

    @staticmethod
    def does_instance_require_reminder(ical_instance: iCalComponent) -> bool:
        if isinstance(ical_instance, VEvent):
            event_title = ical_instance.summary.value
            is_focus_time = "dev time" == event_title.lower() or "focus time" == event_title.lower()
            return not is_focus_time
        if isinstance(ical_instance, VToDo):
            return True
        logger.info("We currently only support VEvents and VToDos.")
        return False
