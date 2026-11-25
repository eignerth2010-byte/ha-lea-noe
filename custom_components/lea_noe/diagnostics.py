"""Diagnostics intentionally exclude all account identifiers and alarm content."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import VERSION


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict:
    coordinator = entry.runtime_data
    return {
        "integration_version": VERSION,
        "read_only_runtime": True,
        "last_update_success": coordinator.last_update_success,
        "poll_interval_seconds": coordinator.update_interval.total_seconds(),
        "details_enabled": coordinator.include_details,
        "notifications_in_window": len(coordinator.data.notifications) if coordinator.data else 0,
        "remembered_identifiers": len(coordinator.seen.serialize()["ids"]),
    }

