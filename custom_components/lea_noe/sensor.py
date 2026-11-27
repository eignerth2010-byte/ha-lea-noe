"""Read-only sensors. Inbox count is deliberately not called active incidents."""

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import LeaEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = entry.runtime_data
    async_add_entities([
        LeaLatestSensor(coordinator), LeaInboxCountSensor(coordinator),
        LeaFetchTimeSensor(coordinator),
        LeaAlarmGroupsSensor(coordinator),
    ])


class LeaLatestSensor(LeaEntity, SensorEntity):
    _attr_translation_key = "latest_notification"
    _attr_icon = "mdi:fire-alert"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "latest_notification")

    @property
    def native_value(self):
        latest = self.coordinator.data.latest
        return latest.label if latest else "Keine Meldungen"

    @property
    def extra_state_attributes(self):
        latest = self.coordinator.data.latest
        return latest.attributes(self.coordinator.include_details) if latest else {}


class LeaInboxCountSensor(LeaEntity, SensorEntity):
    _attr_translation_key = "inbox_count"
    _attr_icon = "mdi:inbox"
    _attr_native_unit_of_measurement = "Meldungen"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "inbox_count")

    @property
    def native_value(self):
        return len(self.coordinator.data.notifications)


class LeaFetchTimeSensor(LeaEntity, SensorEntity):
    _attr_translation_key = "last_fetch"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "last_fetch")

    @property
    def native_value(self):
        return self.coordinator.data.fetched_at


class LeaAlarmGroupsSensor(LeaEntity, SensorEntity):
    _attr_translation_key = "alarm_groups"
    _attr_icon = "mdi:account-group"
    _attr_native_unit_of_measurement = "Gruppen"
    _unrecorded_attributes = frozenset({"alarmgruppen", "aktualisiert_am"})

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "alarm_groups")

    @property
    def available(self):
        return super().available and self.coordinator.data.groups_available

    @property
    def native_value(self):
        return len(self.coordinator.data.groups)

    @property
    def extra_state_attributes(self):
        snapshot = self.coordinator.data
        return {"alarmgruppen": [group.attributes() for group in snapshot.groups],
                "aktualisiert_am": snapshot.groups_updated_at.isoformat() if snapshot.groups_updated_at else None}

