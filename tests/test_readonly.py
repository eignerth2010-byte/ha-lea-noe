"""Offline protocol tests against scripted HTTP responses, without a HA runtime.

Run: python -m unittest discover -s tests -v
The package loader deliberately skips HA's integration bootstrap. This verifies
the actual API/model/dedup code without pretending to be an installed HA core.
"""

import asyncio
from dataclasses import asdict
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
package = types.ModuleType("lea_protocol_test")
package.__path__ = [str(ROOT / "custom_components" / "lea_noe")]
sys.modules[package.__name__] = package
api = importlib.import_module("lea_protocol_test.api")
models = importlib.import_module("lea_protocol_test.models")
dedup = importlib.import_module("lea_protocol_test.dedup")


class FakeResponse:
    def __init__(self, body, status=200, headers=None):
        self.status = status
        self.headers = headers or {}
        self.body = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.content = self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def iter_chunked(self, size):
        for offset in range(0, len(self.body), size):
            yield self.body[offset:offset + size]


class FakeSession:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def request(self, method, url, **kwargs):
        self.requests.append((method, url, kwargs))
        if not self.responses:
            raise AssertionError("Unexpected HTTP request")
        return self.responses.pop(0)


def notification(identifier="new", kind=100, incident="TEST-123", stamp="2026-11-25T18:00:00+01:00"):
    return {"uuid": identifier, "einsatznummer": incident, "nachrichtenartId": kind, "zeitstempel": stamp}


def projected(identifier="new", kind=100):
    return models.project_notification(notification(identifier, kind), {}, {}, False)


class ReadOnlyTests(unittest.IsolatedAsyncioTestCase):
    async def test_runtime_never_authenticates_or_writes(self):
        session = FakeSession()
        client = api.LeaClient(session, "PRIVATE_TOKEN")
        for method, path in [
            ("POST", "/devices"), ("POST", "/sessions"),
            ("PUT", "/incidents"), ("DELETE", "/sessions/current"),
            ("POST", "/notifications"), ("GET", "/devices/current/push-token"),
            ("GET", "/incidents/../sessions"), ("GET", "/incidents?other=1"),
        ]:
            with self.subTest(method=method, path=path):
                with self.assertRaises(api.LeaAccessError):
                    await client._request(method, path)
        self.assertEqual(session.requests, [])
        self.assertNotIn("PRIVATE_TOKEN", repr(client))

    async def test_auth_only_enables_the_two_confirmed_paths(self):
        session = FakeSession()
        client = api.LeaClient(session, allow_auth=True)
        with self.assertRaises(api.LeaAccessError):
            await client._request("POST", "/notifications/receipts")
        self.assertFalse(session.requests)

    async def test_sms_and_login_match_app_payloads(self):
        session = FakeSession(FakeResponse({"message": "Code sent"}), FakeResponse({"token": "PRIVATE_TOKEN"}))
        client = api.LeaClient(session, allow_auth=True)
        await client.request_code("+436641234567")
        result = await client.login("+436641234567", "12345")
        self.assertEqual(result, "PRIVATE_TOKEN")
        self.assertEqual(session.requests[0][2]["json"], {
            "telefonnummer": "+436641234567", "platform": "ios", "pushNotificationToken": "",
        })
        self.assertEqual(session.requests[1][2]["json"], {
            "telefonnummer": "+436641234567", "platform": "ios", "pushNotificationToken": None, "smsToken": "12345",
        })
        self.assertTrue(all(not item[2]["allow_redirects"] for item in session.requests))

    async def test_personal_inbox_is_not_expanded_to_other_recipients(self):
        own = notification()
        own["nachricht"] = "PRIVATE_ALARM_TEXT"
        session = FakeSession(
            FakeResponse({"items": [own, own]}),
            FakeResponse({"items": [{
                "einsatznummer": "TEST-123", "alarmstufe": "T1", "einsatzart": "Technisch",
                "einsatzort": "PRIVATE_ADDRESS", "fluechtig": {"patienten": [{"zuname": "PRIVATE_PATIENT"}]},
                "notifications": [notification("other-recipient"), own],
            }]}),
        )
        snapshot = await api.LeaClient(session, "PRIVATE_TOKEN").fetch_snapshot()
        self.assertEqual(len(snapshot.notifications), 1)
        self.assertEqual(snapshot.latest.category, "alarm")
        self.assertEqual(snapshot.latest.alarm_level, "T1")
        serialized = json.dumps(asdict(snapshot.latest), default=str)
        for private in ["PRIVATE_PATIENT", "PRIVATE_ADDRESS", "PRIVATE_ALARM_TEXT", "PRIVATE_TOKEN"]:
            self.assertNotIn(private, serialized)
        self.assertNotIn("nachricht", snapshot.latest.attributes())
        for method, url, kwargs in session.requests:
            self.assertEqual(method, "GET")
            self.assertTrue(url.startswith("https://lea.api.notrufnoe.at/"))
            self.assertEqual(kwargs["headers"]["Api-Version"], "2")
            self.assertFalse(kwargs["allow_redirects"])

    async def test_optional_details_are_an_explicit_projection(self):
        own = {**notification(), "nachricht": "Text &amp; Hinweis", "patientennamen": ["PRIVATE_PATIENT"]}
        session = FakeSession(FakeResponse({"items": [own]}), FakeResponse({"items": []}))
        snapshot = await api.LeaClient(session).fetch_snapshot(include_details=True)
        self.assertEqual(snapshot.latest.attributes(True)["nachricht"], "Text & Hinweis")
        self.assertNotIn("PRIVATE_PATIENT", repr(snapshot))

    async def test_an_empty_inbox_is_a_valid_baseline(self):
        session = FakeSession(FakeResponse({"items": []}))
        result = await api.LeaClient(session).fetch_snapshot()
        self.assertIsNone(result.latest)
        self.assertEqual(len(session.requests), 1)

    async def test_bad_item_list_does_not_become_an_empty_inbox(self):
        for body in [{}, {"items": None}, {"items": "wrong"}, {"items": [None]}]:
            with self.subTest(body=body):
                with self.assertRaises(api.LeaProtocolError):
                    await api.LeaClient(FakeSession(FakeResponse(body))).fetch_snapshot()

    async def test_missing_stable_id_is_an_error(self):
        session = FakeSession(FakeResponse({"items": [{"einsatznummer": "123"}]}), FakeResponse({"items": []}))
        with self.assertRaises(api.LeaProtocolError):
            await api.LeaClient(session).fetch_snapshot()

    async def test_http_errors_are_sanitized_and_distinct(self):
        for status, error_type in [(401, api.LeaAuthError), (403, api.LeaAccessError), (500, api.LeaConnectionError), (302, api.LeaProtocolError)]:
            with self.subTest(status=status):
                session = FakeSession(FakeResponse({"error": "PRIVATE_TOKEN PRIVATE_PATIENT"}, status))
                with self.assertRaises(error_type) as caught:
                    await api.LeaClient(session).get_profile()
                self.assertNotIn("PRIVATE", str(caught.exception))

    async def test_wrong_sms_is_auth_error(self):
        session = FakeSession(FakeResponse({"error": "PRIVATE"}, 400))
        with self.assertRaises(api.LeaAuthError):
            await api.LeaClient(session, allow_auth=True).login("+436641234567", "99999")

    async def test_rate_limit_honors_retry_after(self):
        session = FakeSession(FakeResponse({"erneutMoeglichInSekunden": 42}, 429, {"Retry-After": "120"}))
        with self.assertRaises(api.LeaRateLimitError) as caught:
            await api.LeaClient(session).get_profile()
        self.assertEqual(caught.exception.retry_after, 120)
        self.assertEqual(api.retry_seconds(None, {"erneutMoeglichInSekunden": 42}), 42)

    async def test_invalid_json_and_oversized_response(self):
        for raw in [b"not JSON", b"x" * (api.LeaClient.MAX_BODY + 1)]:
            with self.assertRaises(api.LeaProtocolError):
                await api.LeaClient(FakeSession(FakeResponse(raw))).get_profile()

    async def test_no_session_token_is_not_success(self):
        with self.assertRaises(api.LeaProtocolError):
            await api.LeaClient(FakeSession(FakeResponse({"message": "not logged in"})), allow_auth=True).login("+436641234567", "12345")

    async def test_transport_errors_do_not_leak_credentials(self):
        class BrokenSession:
            def request(self, *args, **kwargs):
                raise OSError("PRIVATE_TOKEN in an underlying transport error")
        with self.assertRaises(api.LeaConnectionError) as caught:
            await api.LeaClient(BrokenSession()).get_profile()
        self.assertNotIn("PRIVATE_TOKEN", str(caught.exception))


class ModelTests(unittest.TestCase):
    def test_coordinates_require_details_and_are_not_in_basic_event_attributes(self):
        incident = {"positionX": "48.2", "positionY": "16.3"}
        hidden = models.project_notification(notification(), incident, {}, False)
        self.assertIsNone(hidden.latitude)
        self.assertNotIn("latitude", hidden.attributes())
        visible = models.project_notification(notification(), incident, {}, True)
        self.assertEqual(visible.attributes(True)["latitude"], 48.2)
        self.assertEqual(visible.attributes(True)["longitude"], 16.3)
        self.assertNotIn("latitude", visible.attributes())

    def test_invalid_coordinates_are_not_exposed(self):
        for value in [True, "nan", "inf", "-inf", "https://example.com", 91, -91, {}, []]:
            self.assertIsNone(models.coordinate(value, 90))
        self.assertEqual(models.coordinate("0", 90), 0)

    def test_phone_normalization(self):
        self.assertEqual(models.normalize_phone("0664 / 1234567"), "+436641234567")
        self.assertEqual(models.normalize_phone("00436641234567"), "+436641234567")
        for value in ["", "abc", "+123", "+43x6641234567"]:
            with self.assertRaises(ValueError):
                models.normalize_phone(value)

    def test_timestamps_and_unknown_timezone(self):
        a = models.parse_timestamp("2026-11-25T18:00:00+01:00")
        b = models.parse_timestamp("2026-11-25T17:00:00Z")
        self.assertEqual(a, b)
        self.assertEqual(models.parse_timestamp(int(a.timestamp() * 1000)), a)
        self.assertIsNone(models.parse_timestamp("2026-11-25T18:00:00"))
        self.assertIsNone(models.parse_timestamp("invalid"))

    def test_type_mapping_is_from_the_app_not_inferred_from_alarm_level(self):
        for kind, expected in [(100, "alarm"), (60, "alarm"), (10, "information"), (30, "cancellation"), (20, "message"), (40, "message"), (999, "unknown")]:
            self.assertEqual(projected(kind=kind).category, expected)
        own = {"uuid": "old", "einsatznummer": "123"}
        projection = models.project_notification(own, {"nachrichtenartId": 100, "zeitstempel": "2026-11-25T17:00:00Z"}, {}, False)
        self.assertEqual(projection.category, "unknown")
        self.assertIsNone(projection.timestamp)

    def test_first_start_suppresses_history_but_empty_baseline_allows_first_alarm(self):
        seen = dedup.SeenNotifications()
        self.assertEqual(seen.observe((projected("old"),)), [])
        self.assertEqual([item.identifier for item in seen.observe((projected("new"), projected("old")))], ["uuid:new"])
        empty = dedup.SeenNotifications()
        empty.observe(())
        self.assertEqual(len(empty.observe((projected(),))), 1)

    def test_restart_does_not_replay_and_new_ids_on_same_incident_survive(self):
        seen = dedup.SeenNotifications()
        seen.observe((projected("old"),))
        restored = dedup.SeenNotifications(json.loads(json.dumps(seen.serialize())))
        result = restored.observe((projected("cancel", 30), projected("update"), projected("old")))
        self.assertEqual([item.identifier for item in result], ["uuid:update", "uuid:cancel"])
        self.assertFalse(restored.observe((projected("cancel", 30), projected("update"))))
        self.assertNotIn("nachricht", str(restored.serialize()))

    def test_seen_id_storage_is_bounded(self):
        seen = dedup.SeenNotifications()
        seen.observe(tuple(projected(str(index)) for index in range(2100)))
        self.assertEqual(len(seen.serialize()["ids"]), 2000)


if __name__ == "__main__":
    unittest.main()

