"""Local HA sound playback. This module has no LEA client or HTTP write path."""

from __future__ import annotations

import asyncio
from contextlib import suppress
import logging
from typing import Callable

from .const import (
    CONF_AUDIO_DURATION, CONF_AUDIO_ENABLED, CONF_AUDIO_PLAYERS,
    CONF_AUDIO_SOUND, CONF_AUDIO_VOLUME, DEFAULT_AUDIO_SOUND,
)
from .sounds import SOUNDS

_LOGGER = logging.getLogger(__name__)
# Home Assistant's MediaPlayerEntityFeature flags (Core 2026.11).
PLAY_MEDIA = 512
VOLUME_SET = 4
STOP = 4096


class AlarmPlaybackError(Exception):
    """A local playback setup or device error; contains no alarm contents."""


def audio_settings(options: dict) -> dict:
    """Validate persisted options again before using them as service targets."""
    players = options.get(CONF_AUDIO_PLAYERS, [])
    if not isinstance(players, list):
        players = []
    players = list(dict.fromkeys(
        value for value in players if isinstance(value, str)
        and value.startswith("media_player.") and value.count(".") == 1
        and value.replace("media_player.", "", 1).replace("_", "").isalnum()
    ))
    sound = options.get(CONF_AUDIO_SOUND, DEFAULT_AUDIO_SOUND)
    if not isinstance(sound, str) or sound not in SOUNDS:
        sound = DEFAULT_AUDIO_SOUND
    try:
        volume = max(0, min(100, int(options.get(CONF_AUDIO_VOLUME, 50))))
    except (ValueError, TypeError, OverflowError):
        volume = 50
    try:
        duration = int(options.get(CONF_AUDIO_DURATION, 0))
    except (ValueError, TypeError, OverflowError):
        duration = 0
    if duration not in (0, 10, 30, 60):
        duration = 0
    return {
        "enabled": options.get(CONF_AUDIO_ENABLED) is True,
        "players": players, "sound": sound,
        "volume": volume, "duration": duration,
    }


def has_alarm(notifications) -> bool:
    return any(item.category == "alarm" for item in notifications)


class LeaAlarmPlayer:
    """One bounded, cancellable playback per account, independent of the panel."""

    def __init__(self, hass, entry, get_base_url: Callable[[], str]) -> None:
        self.hass = hass
        self.entry = entry
        self._get_base_url = get_base_url
        self._lock = asyncio.Lock()
        self._task: asyncio.Task | None = None
        self._started: dict[str, dict] = {}
        self._closed = False

    @property
    def settings(self) -> dict:
        return audio_settings(self.entry.options)

    async def async_handle(self, notifications) -> None:
        settings = self.settings
        if self._closed or not settings["enabled"] or not has_alarm(notifications):
            return
        if SOUNDS[settings["sound"]]["silent"]:
            return
        try:
            await self.async_play()
        except AlarmPlaybackError:
            _LOGGER.warning("LEA-Alarmton konnte auf keinem konfigurierten HA-Gerät gestartet werden")

    async def _service(self, name: str, entity_id: str, data: dict | None = None) -> None:
        await self.hass.services.async_call(
            "media_player", name, {"entity_id": entity_id, **(data or {})}, blocking=True,
        )

    async def async_play(self) -> None:
        """Explicit test works with auto playback disabled; configuration is shared."""
        async with self._lock:
            if self._closed:
                raise AlarmPlaybackError("Die LEA-Integration wird gerade entladen.")
            await self._stop_locked()
            settings = self.settings
            sound = SOUNDS[settings["sound"]]
            if sound["silent"]:
                raise AlarmPlaybackError("Der gewählte Ton ist lautlos. Bitte einen hörbaren Ton auswählen.")
            players = []
            for entity_id in settings["players"]:
                state = self.hass.states.get(entity_id)
                if state and state.state not in ("unavailable", "unknown"):
                    if int(state.attributes.get("supported_features", 0)) & PLAY_MEDIA:
                        players.append((entity_id, state))
            if not players:
                raise AlarmPlaybackError("Bitte in den LEA-Optionen ein verfügbares Wiedergabegerät auswählen.")
            try:
                base = self._get_base_url().rstrip("/")
            except Exception:
                raise AlarmPlaybackError("Home Assistant hat keine erreichbare Basisadresse für die Audiodateien.") from None
            url = f"{base}/lea-noe-static/sounds/{sound['file']}"
            for entity_id, state in players:
                record = {"url": url, "old_volume": None, "set_volume": settings["volume"] / 100}
                try:
                    if int(state.attributes.get("supported_features", 0)) & VOLUME_SET:
                        old = state.attributes.get("volume_level")
                        if isinstance(old, (int, float)) and not isinstance(old, bool) and 0 <= old <= 1:
                            record["old_volume"] = old
                        await self._service("volume_set", entity_id, {"volume_level": record["set_volume"]})
                    self._started[entity_id] = record
                    await self._service("play_media", entity_id, {
                        "media": {"media_content_id": url, "media_content_type": "music"},
                    })
                except Exception:
                    await self._cleanup_player(entity_id, stop=False)
                    _LOGGER.warning("LEA-Tonwiedergabe auf einem HA-Gerät fehlgeschlagen")
            if not self._started:
                raise AlarmPlaybackError("Keines der gewählten Geräte hat den Wiedergabebefehl angenommen.")
            # A duration is an upper bound, not an endless repeat or a loop.
            natural = float(sound["seconds"]) + 1.5
            seconds = min(natural, settings["duration"]) if settings["duration"] else natural
            self._task = self.hass.async_create_task(self._finish_after(seconds))

    async def _finish_after(self, seconds: float) -> None:
        try:
            await asyncio.sleep(seconds)
        finally:
            await self._cleanup()

    async def _cleanup_player(self, entity_id: str, *, stop: bool = True) -> None:
        record = self._started.pop(entity_id, None)
        if not record:
            return
        state = self.hass.states.get(entity_id)
        if not state:
            return
        current_media = state.attributes.get("media_content_id")
        # Do not stop a different track started by the user in the meantime.
        if stop and state.state == "playing" and (not current_media or current_media == record["url"]):
            if int(state.attributes.get("supported_features", 0)) & STOP:
                with suppress(Exception):
                    await self._service("media_stop", entity_id)
        old = record["old_volume"]
        current = state.attributes.get("volume_level")
        if old is not None and isinstance(current, (int, float)):
            # Respect a manual volume change made during the alarm.
            if abs(current - record["set_volume"]) < 0.005:
                with suppress(Exception):
                    await self._service("volume_set", entity_id, {"volume_level": old})

    async def _cleanup(self) -> None:
        for entity_id in list(self._started):
            await self._cleanup_player(entity_id)

    async def _stop_locked(self) -> None:
        if self._task:
            task, self._task = self._task, None
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        await self._cleanup()

    async def async_stop(self) -> None:
        async with self._lock:
            await self._stop_locked()

    async def async_shutdown(self) -> None:
        self._closed = True
        await self.async_stop()
