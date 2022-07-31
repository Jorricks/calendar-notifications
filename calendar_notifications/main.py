from __future__ import annotations

import logging
import time
from typing import List

from ical_library import client
from ical_library.ical_components import VCalendar, VEvent, VToDo
from ical_library.timeline import Timeline
from pendulum import DateTime, Duration

from calendar_notifications.cn_configuration import CNConfiguration

root_logger = logging.getLogger()
root_logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
root_logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


def sleep_until(future: DateTime):
    """Sleep till 'future' is present."""
    logger.info(f"Sleep for {DateTime.now().diff_for_humans(future, absolute=True)}.")
    time.sleep((future - DateTime.now()).total_seconds() + 1)


def get_next_ical_component(ical_components_these_7_days: List[VEvent | VToDo]) -> VEvent | VToDo | None:
    """Get the upcoming iCalendar event. Note: we assume that all_status_changes is sorted."""
    for start_status_change in ical_components_these_7_days:
        if start_status_change.start > DateTime.now():
            return start_status_change
    return None


def get_events_in_upcoming_week() -> List[VEvent | VToDo]:
    """Gets the calendar events in the upcoming 7 days."""
    logger.info("Loading your calendar, this might take some time.")
    now = DateTime.now()
    week_from_now = now + Duration(days=7)
    calendar: VCalendar = client.parse_icalendar_url(CNConfiguration().private_ical_url)
    timeline: Timeline = calendar.get_limited_timeline(now, week_from_now)
    return [item for item in timeline.overlapping(now, week_from_now) if isinstance(item, (VEvent, VToDo))]


def main() -> None:
    """
    The main loop which checks for notifications it should show and shows them.
    Note: Currently we only support one event at a time.

    When you run this, we automatically invoke a CNConfiguration. If you want to set different values, you should
    initialise the CNConfiguration beforehand, and it will automatically be picked up by our application.
    """
    next_event: VEvent | VToDo | None = None
    while True:
        while next_event is None or (next_event.start - DateTime.now()) > Duration(minutes=20):
            if next_event is not None:
                logger.debug("No event planned for the next 20 minutes. Refreshing in 15 minutes.")
                time.sleep(15 * 60)
            schema = get_events_in_upcoming_week()
            print("DONE")
            logger.debug("Done loading your calendar.")
            next_event = get_next_ical_component(schema)

        if next_event is None:
            raise ValueError("No event planned in the upcoming 7 days.. Are you on holiday or what?")
        logger.info(f"Next up is: {next_event}.")
        sleep_until(next_event.start)
        CNConfiguration().event_start_handler.run(next_event)


if __name__ == "__main__":
    main()
