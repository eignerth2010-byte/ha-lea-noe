"""One shared read poll, explicit error states and persistent replay protection."""

from collections import deque
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import LeaAccessError, LeaAuthError, LeaClient, LeaError, LeaRateLimitError
from .const import CONF_DETAILS, CONF_INTERVAL, DEFAULT_INTERVAL, DOMAIN, MAX_INTERVAL, MIN_INTERVAL
from .dedup import SeenNotifications
from .models import Notification, Snapshot

_LOGGER = logging.getLogger(__name__)


class LeaCoordinator(DataUpdateCoordinator[Snapshot]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: LeaClient) -> None:
        interval = max(MIN_INTERVAL, min(MAX_INTERVAL, int(entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL))))
        super().__init__(
            hass, _LOGGER, name=DOMAIN, config_entry=entry,
            update_interval=timedelta(seconds=interval),
        )
        self.client = client
        self.entry = entry
        self.include_details = bool(entry.options.get(CONF_DETAILS, False))
        self.seen = SeenNotifications()
        self.pending: deque[Notification] = deque(maxlen=200)
        self.audio = None
        self._store = Store(hass, 1, f"{DOMAIN}.{entry.entry_id}.seen")

    async def async_load_seen(self) -> None:
        self.seen = SeenNotifications(await self._store.async_load())

    async def async_save_seen(self) -> None:
        await self._store.async_save(self.seen.serialize())

    async def _async_update_data(self) -> Snapshot:
        try:
            snapshot = await self.client.fetch_snapshot(include_details=self.include_details)
        except LeaAuthError as err:
            raise ConfigEntryAuthFailed("LEA-Sitzung abgelaufen. Bitte erneut anmelden.") from err
        except LeaRateLimitError as err:
            raise UpdateFailed("LEA begrenzt die Abrufrate.", retry_after=err.retry_after) from err
        except LeaAccessError as err:
            raise UpdateFailed("LEA verweigert den Lesezugriff.") from err
        except LeaError as err:
            raise UpdateFailed(str(err)) from err
        new_notifications = self.seen.observe(snapshot.notifications)
        self.pending.extend(new_notifications)
        if self.audio and new_notifications:
            self.hass.async_create_task(self.audio.async_handle(new_notifications))
        self._store.async_delay_save(self.seen.serialize, 5)
        return snapshot

