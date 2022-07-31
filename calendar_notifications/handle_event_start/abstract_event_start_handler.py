from __future__ import annotations

from abc import ABC, abstractmethod

from ical_library.base_classes.component import Component as iCalComponent


class AbstractEventStartHandler(ABC):
    @staticmethod
    @abstractmethod
    def play_notification_sound(ical_instance: iCalComponent):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_notification_on_mac(ical_instance: iCalComponent) -> None:
        raise NotImplementedError()

    @staticmethod
    def extra_operation(ical_instance: iCalComponent) -> None:
        pass

    @staticmethod
    def does_instance_require_reminder(ical_instance: iCalComponent) -> bool:
        return True

    @classmethod
    def run(cls, ical_instance: iCalComponent) -> None:
        if cls.does_instance_require_reminder(ical_instance):
            cls.create_notification_on_mac(ical_instance)
            cls.play_notification_sound(ical_instance)
            cls.extra_operation(ical_instance)
