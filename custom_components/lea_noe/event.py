"""New personal notifications, using HA's native event entity."""

from homeassistant.components.event import EventEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import EVENT_TYPES
from .entity import LeaEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([LeaNotificationEvent(entry.runtime_data)])


class LeaNotificationEvent(LeaEntity, EventEntity):
    _attr_translation_key = "notification"
    _attr_event_types = EVENT_TYPES
    _attr_icon = "mdi:alarm-light"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "notification")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._publish_pending()

    @callback
    def _publish_pending(self) -> None:
        while self.coordinator.pending:
            item = self.coordinator.pending.popleft()
            # Event entities restore their last attributes. Keep alarm text and
            # locations out of that persistent event state, even when the last
            # notification sensor's optional detail view is enabled.
            self._trigger_event(item.category, item.attributes())
            self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        if self.coordinator.last_update_success:
            self._publish_pending()
        super()._handle_coordinator_update()

