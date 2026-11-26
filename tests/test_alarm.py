"""Exercise local playback with a fake HA service bus, without touching LEA."""

import asyncio
import hashlib
import importlib
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
package = ModuleType("lea_alarm_test")
package.__path__ = [str(ROOT / "custom_components" / "lea_noe")]
sys.modules[package.__name__] = package
alarm = importlib.import_module("lea_alarm_test.alarm")
sounds = importlib.import_module("lea_alarm_test.sounds").SOUNDS


class FakeHass:
    def __init__(self):
        self.values = {
            "media_player.tablet": SimpleNamespace(state="idle", attributes={"supported_features": 4612, "volume_level": .2}),
            "media_player.other": SimpleNamespace(state="idle", attributes={"supported_features": 4612, "volume_level": .3}),
        }
        self.calls = []
        self.fail = set()
        self.states = SimpleNamespace(get=self.values.get)
        self.services = SimpleNamespace(async_call=self.async_call)

    def async_create_task(self, coroutine):
        return asyncio.create_task(coroutine)

    async def async_call(self, domain, service, data, blocking):
        assert domain == "media_player" and blocking
        entity = data["entity_id"]
        self.calls.append((service, entity, data))
        if entity in self.fail and service == "play_media":
            raise RuntimeError("device failed")
        state = self.values[entity]
        if service == "volume_set":
            state.attributes["volume_level"] = data["volume_level"]
        elif service == "play_media":
            state.state = "playing"
            state.attributes["media_content_id"] = data["media"]["media_content_id"]
        elif service == "media_stop":
            state.state = "idle"


class SoundCatalogueTests(unittest.TestCase):
    def test_bundled_files_are_original_and_catalogue_is_bounded(self):
        self.assertEqual(len(sounds), 38)
        for key, item in sounds.items():
            self.assertEqual(key, item["id"])
            self.assertNotIn("/", item["file"])
            data = (ROOT / "custom_components/lea_noe/frontend/sounds" / item["file"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
            self.assertGreater(item["seconds"], 0)
            self.assertLess(item["seconds"], 120)
        self.assertEqual([k for k, v in sounds.items() if v["silent"]], ["lautlos"])

    def test_invalid_options_cannot_become_urls_or_service_targets(self):
        result = alarm.audio_settings({
            "audio_enabled": "true", "audio_sound": ["../../token"],
            "audio_players": ["light.any", "media_player.good", "media_player.good", "media_player.bad/path", "media_player."],
            "audio_volume": 999, "audio_duration": 100000,
        })
        self.assertEqual(result["players"], ["media_player.good"])
        self.assertEqual(result["sound"], "fwprio1")
        self.assertEqual(result["volume"], 100)
        self.assertEqual(result["duration"], 0)
        self.assertFalse(result["enabled"])


class PlaybackTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.hass = FakeHass()
        self.entry = SimpleNamespace(options={"audio_players": ["media_player.tablet"], "audio_volume": 60})
        self.player = alarm.LeaAlarmPlayer(self.hass, self.entry, lambda: "https://ha.example.invalid/")

    async def asyncTearDown(self):
        await self.player.async_shutdown()

    async def test_disabled_or_non_alarm_notifications_never_play(self):
        await self.player.async_handle([SimpleNamespace(category="alarm")])
        self.entry.options["audio_enabled"] = True
        for kind in ["information", "message", "cancellation", "unknown"]:
            await self.player.async_handle([SimpleNamespace(category=kind)])
        self.assertEqual(self.hass.calls, [])

    async def test_new_alarm_plays_without_an_open_frontend(self):
        self.entry.options["audio_enabled"] = True
        await self.player.async_handle([SimpleNamespace(category="alarm")])
        play = [data for service, _, data in self.hass.calls if service == "play_media"]
        self.assertEqual(len(play), 1)
        self.assertEqual(play[0]["media"]["media_content_id"], "https://ha.example.invalid/lea-noe-static/sounds/fwprio1.mp3")

    async def test_explicit_preview_works_while_auto_playback_is_disabled(self):
        await self.player.async_play()
        self.assertEqual(self.hass.values["media_player.tablet"].attributes["volume_level"], .6)
        await asyncio.sleep(0)
        await self.player.async_stop()
        self.assertEqual(self.hass.values["media_player.tablet"].state, "idle")
        self.assertEqual(self.hass.values["media_player.tablet"].attributes["volume_level"], .2)

    async def test_no_available_target_reports_a_local_error(self):
        self.hass.values["media_player.tablet"].state = "unavailable"
        with self.assertRaises(alarm.AlarmPlaybackError):
            await self.player.async_play()
        self.assertEqual(self.hass.calls, [])

    async def test_one_failing_device_does_not_prevent_the_other(self):
        self.entry.options["audio_players"] = ["media_player.tablet", "media_player.other"]
        self.hass.fail.add("media_player.tablet")
        await self.player.async_play()
        self.assertEqual(self.hass.values["media_player.other"].state, "playing")
        self.assertEqual(self.hass.values["media_player.tablet"].attributes["volume_level"], .2)

    async def test_manual_changes_are_respected_when_stopping(self):
        await self.player.async_play()
        await asyncio.sleep(0)
        state = self.hass.values["media_player.tablet"]
        state.attributes["media_content_id"] = "https://example.invalid/my-track.mp3"
        state.attributes["volume_level"] = .4
        await self.player.async_stop()
        self.assertEqual(state.state, "playing")
        self.assertEqual(state.attributes["volume_level"], .4)

    async def test_silent_choice_does_not_play_an_automatic_alarm(self):
        self.entry.options.update(audio_enabled=True, audio_sound="lautlos")
        await self.player.async_handle([SimpleNamespace(category="alarm")])
        self.assertEqual(self.hass.calls, [])
        with self.assertRaises(alarm.AlarmPlaybackError):
            await self.player.async_play()

    async def test_shutdown_prevents_delayed_automatic_playback(self):
        self.entry.options["audio_enabled"] = True
        await self.player.async_shutdown()
        await self.player.async_handle([SimpleNamespace(category="alarm")])
        self.assertEqual(self.hass.calls, [])
        with self.assertRaises(alarm.AlarmPlaybackError):
            await self.player.async_play()


if __name__ == "__main__":
    unittest.main()
