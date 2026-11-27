"""Personal alarm groups projected from GET /me; no member/person records."""

from dataclasses import dataclass
from .models import text


@dataclass(frozen=True, slots=True)
class AlarmGroup:
    identifier: str
    name: str
    organisation_id: str
    organisation: str
    unit_id: str
    unit: str
    dynamic: bool

    def attributes(self) -> dict:
        return {
            "id": self.identifier, "name": self.name,
            "organisation_id": self.organisation_id, "organisation": self.organisation,
            "organisationseinheit_id": self.unit_id, "organisationseinheit": self.unit,
            "dynamisch": self.dynamic,
        }


def project_alarm_groups(profile: dict) -> tuple[AlarmGroup, ...]:
    """Use personal top-level membership, as the app's configuration tree does.

    Nested organisation groups alone are not proof of personal membership.
    Never infer membership or invent a group ID from a displayed name.
    """
    rows = profile.get("alarmgruppen")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("Missing or malformed personal alarm-group list")
    units = {}
    organisations = profile.get("organisationen", [])
    if isinstance(organisations, list):
        for organisation in organisations:
            if not isinstance(organisation, dict):
                continue
            children = organisation.get("organisationseinheiten", [])
            if not isinstance(children, list):
                continue
            for unit in children:
                if isinstance(unit, dict) and (unit_id := text(unit.get("id"), 128)):
                    units[unit_id] = (
                        text(organisation.get("id"), 128),
                        text(organisation.get("bezeichnung"), 256),
                        text(unit.get("bezeichnung"), 256),
                    )
    groups = {}
    for row in rows:
        identifier = text(row.get("id"), 128)
        if not identifier:
            raise ValueError("Personal alarm group without an ID")
        unit_id = text(row.get("organisationseinheitenId"), 128)
        org_id, org_name, unit_name = units.get(unit_id, ("", "", ""))
        group = AlarmGroup(identifier, text(row.get("beschreibung"), 512),
                           org_id, org_name, unit_id, unit_name, row.get("dynamic") is True)
        if identifier in groups and groups[identifier] != group:
            raise ValueError("Conflicting personal alarm-group IDs")
        groups[identifier] = group
    return tuple(groups.values())
