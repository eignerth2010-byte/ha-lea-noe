"""Persist identifiers, not alarm text, to avoid replaying the inbox on restart."""

from collections import OrderedDict
from .models import Notification


class SeenNotifications:
    MAX_IDS = 2000

    def __init__(self, saved: dict | None = None) -> None:
        saved = saved if isinstance(saved, dict) else {}
        ids = saved.get("ids", [])
        self._ids = OrderedDict.fromkeys(
            value for value in (ids if isinstance(ids, list) else [])
            if isinstance(value, str)
        )
        self.initialized = saved.get("initialized") is True
        self._trim()

    def _trim(self) -> None:
        while len(self._ids) > self.MAX_IDS:
            self._ids.popitem(last=False)

    def observe(self, notifications: tuple[Notification, ...]) -> list[Notification]:
        new: list[Notification] = []
        # Input is newest first. Publish multiple arrivals in chronological order.
        for notification in reversed(notifications):
            if notification.identifier not in self._ids:
                if self.initialized:
                    new.append(notification)
                self._ids[notification.identifier] = None
            else:
                self._ids.move_to_end(notification.identifier)
        self.initialized = True
        self._trim()
        return new

    def serialize(self) -> dict:
        return {"initialized": self.initialized, "ids": list(self._ids)}

