"""Unofficial, read-only LEA BOS mobil integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.network import get_url

from .api import LeaClient
from .const import CONF_TOKEN, DOMAIN
from .coordinator import LeaCoordinator
from .alarm import LeaAlarmPlayer
from .panel import async_setup_frontend, async_add_entry_panel, async_remove_entry_panel

PLATFORMS = [Platform.SENSOR, Platform.EVENT, Platform.BUTTON]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    await async_setup_frontend(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = LeaClient(async_get_clientsession(hass), entry.data[CONF_TOKEN])
    coordinator = LeaCoordinator(hass, entry, client)
    await coordinator.async_load_seen()
    await coordinator.async_config_entry_first_refresh()
    coordinator.audio = LeaAlarmPlayer(hass, entry, lambda: get_url(hass))
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_add_entry_panel(hass, entry.entry_id, coordinator)
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if entry.runtime_data.audio:
        await entry.runtime_data.audio.async_stop()
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        if entry.runtime_data.audio:
            await entry.runtime_data.audio.async_shutdown()
        async_remove_entry_panel(hass, entry.entry_id)
        await entry.runtime_data.async_save_seen()
    return unloaded


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove only this integration's local replay-protection record."""
    await Store(hass, 1, f"{DOMAIN}.{entry.entry_id}.seen").async_remove()

