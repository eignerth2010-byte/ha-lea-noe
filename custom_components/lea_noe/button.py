"""Test and stop the local HA alarm sound, without generating LEA events."""

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.exceptions import HomeAssistantError

from .alarm import AlarmPlaybackError
from .entity import LeaEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([
        LeaSoundButton(entry.runtime_data, False),
        LeaSoundButton(entry.runtime_data, True),
    ])


class LeaSoundButton(LeaEntity, ButtonEntity):
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator, stop: bool) -> None:
        key = "stop_alarm_sound" if stop else "test_alarm_sound"
        super().__init__(coordinator, key)
        self._stop = stop
        self._attr_translation_key = key
        self._attr_icon = "mdi:stop-circle-outline" if stop else "mdi:volume-high"

    @property
    def available(self) -> bool:
        return self.coordinator.audio is not None

    async def async_press(self) -> None:
        try:
            if self._stop:
                await self.coordinator.audio.async_stop()
            else:
                await self.coordinator.audio.async_play()
        except AlarmPlaybackError as err:
            raise HomeAssistantError(str(err)) from err
