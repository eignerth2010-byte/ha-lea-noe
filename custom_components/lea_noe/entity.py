"""Shared, non-identifying device information."""

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION
from .coordinator import LeaCoordinator


class LeaEntity(CoordinatorEntity[LeaCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: LeaCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.unique_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.unique_id)},
            name=NAME, manufacturer="Notruf Niederösterreich",
            model="Persönlicher LEA-Zugang (inoffiziell, Lesen)",
            sw_version=VERSION, entry_type=DeviceEntryType.SERVICE,
        )

