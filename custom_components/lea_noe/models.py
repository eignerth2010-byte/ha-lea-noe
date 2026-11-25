"""Small, explicit projections of the LEA v2 response; no patient records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
import re
from typing import Any

CATEGORIES = {100: "alarm", 60: "alarm", 10: "information", 30: "cancellation", 20: "message", 40: "message"}
LABELS = {"alarm": "Alarmierung", "information": "Information", "cancellation": "Storno", "message": "Nachricht", "unknown": "Unbekannte Meldungsart"}


def text(value: Any, limit: int = 4096) -> str:
    """Accept scalar text only, with a bounded size."""
    if value is None or isinstance(value, (dict, list, bool)):
        return ""
    return unescape(str(value)).strip()[:limit]


def normalize_phone(value: str) -> str:
    """Normalize Austrian national numbers or an explicit international number."""
    phone = re.sub(r"[\s\-/()]", "", value)
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    elif phone.startswith("0"):
        phone = "+43" + phone[1:]
    if not re.fullmatch(r"\+[1-9][0-9]{7,14}", phone):
        raise ValueError("invalid_phone")
    return phone


def parse_timestamp(value: Any) -> datetime | None:
    """Parse ISO timestamps or Unix seconds/milliseconds, returning UTC."""
    if value is None or isinstance(value, bool):
        return None
    try:
        raw = str(value).strip()
        if re.fullmatch(r"\d{10}(?:\.\d+)?|\d{13}", raw):
            number = float(raw)
            return datetime.fromtimestamp(number / 1000 if number >= 10**12 else number, timezone.utc)
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            # The DTO does not document a timezone for naive timestamps.
            # Keep it unknown instead of fabricating an alarm time.
            return None
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError, OSError):
        return None


@dataclass(frozen=True, slots=True)
class Notification:
    """Whitelisted fields only; never hold an entire server DTO."""

    identifier: str
    incident_number: str
    category: str
    type_id: int | None
    timestamp: datetime | None
    alarm_level: str
    incident_type: str
    keyword: str
    message: str
    location: str

    @property
    def label(self) -> str:
        return LABELS[self.category]

    def attributes(self, include_details: bool = False) -> dict[str, Any]:
        attributes: dict[str, Any] = {
            "meldungs_id": self.identifier,
            "einsatznummer": self.incident_number,
            "meldungsart": self.category,
            "nachrichtenart_id": self.type_id,
            "alarmstufe": self.alarm_level,
            "einsatzart": self.incident_type,
            "zeitstempel": self.timestamp.isoformat() if self.timestamp else None,
        }
        if include_details:
            attributes.update(meldebild=self.keyword, nachricht=self.message, einsatzort=self.location)
        return attributes


def project_notification(inbox: dict, incident: dict, embedded: dict, include_details: bool) -> Notification | None:
    """Join personal inbox records by UUID, never import another person's message."""
    row = {**incident, **embedded, **inbox}
    identifier = text(inbox.get("uuid"), 256)
    if identifier:
        identifier = "uuid:" + identifier
    elif inbox.get("benachrichtigungId") is not None:
        identifier = "id:" + text(inbox["benachrichtigungId"], 256)
    else:
        return None
    try:
        # An incident summary may describe a different, newer notification.
        # Never infer the personal notification's type from that summary.
        type_id = int(inbox.get("nachrichtenartId", embedded.get("nachrichtenartId")))
    except (KeyError, TypeError, ValueError):
        type_id = None
    return Notification(
        identifier=identifier,
        incident_number=text(row.get("einsatznummer"), 128),
        category=CATEGORIES.get(type_id, "unknown"),
        type_id=type_id,
        timestamp=parse_timestamp(inbox.get("zeitstempel") or inbox.get("sentAt") or embedded.get("zeitstempel") or embedded.get("sentAt")),
        alarm_level=text(row.get("alarmstufe"), 32),
        incident_type=text(row.get("einsatzart"), 128),
        keyword=text(row.get("meldebild")) if include_details else "",
        message=text(row.get("nachricht")) if include_details else "",
        location=text(row.get("einsatzort")) if include_details else "",
    )


@dataclass(frozen=True, slots=True)
class Snapshot:
    notifications: tuple[Notification, ...]
    fetched_at: datetime

    @property
    def latest(self) -> Notification | None:
        return self.notifications[0] if self.notifications else None

