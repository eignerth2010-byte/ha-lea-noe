"""Personal-group membership and notification joins, with no live credentials."""

import unittest
from dataclasses import asdict
import json
from test_readonly import api, models, FakeSession, FakeResponse, notification
from lea_protocol_test.groups import project_alarm_groups


def profile():
    return {"id": "test-account", "vorname": "PRIVATE_PERSON", "telefonnummern": ["PRIVATE_PHONE"],
            "organisationen": [{"id": 1, "bezeichnung": "Test-Organisation", "organisationseinheiten": [
                {"id": 2, "bezeichnung": "Test-Einheit", "alarmgruppen": [{"id": 99, "beschreibung": "Other membership"}]}]}],
            "alarmgruppen": [{"id": 42, "beschreibung": "Test-Probe", "organisationseinheitenId": 2,
                              "dynamic": False, "personen": ["PRIVATE_MEMBER"]}]}


class GroupTests(unittest.TestCase):
    def test_only_personal_membership_is_projected(self):
        groups = project_alarm_groups(profile())
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].identifier, "42")
        self.assertEqual(groups[0].unit, "Test-Einheit")
        self.assertEqual(groups[0].organisation, "Test-Organisation")
        self.assertNotIn("PRIVATE", json.dumps([asdict(g) for g in groups]))

    def test_missing_list_is_not_reported_as_no_groups(self):
        for raw in [{}, {"alarmgruppen": None}, {"alarmgruppen": [None]}, {"alarmgruppen": [{}]}]:
            with self.assertRaises(ValueError):
                project_alarm_groups(raw)
        self.assertEqual(project_alarm_groups({"alarmgruppen": []}), ())

    def test_duplicate_ids_deduplicate_but_conflicts_fail(self):
        raw = profile()
        raw["alarmgruppen"] *= 2
        self.assertEqual(len(project_alarm_groups(raw)), 1)
        raw["alarmgruppen"] = [raw["alarmgruppen"][0], {"id": 42, "beschreibung": "Different"}]
        with self.assertRaises(ValueError):
            project_alarm_groups(raw)

    def test_notification_joins_only_its_own_group(self):
        groups = project_alarm_groups(profile())
        own = {**notification(), "alarmgruppenId": 42}
        row = models.project_notification(own, {"alarmgruppenId": 99}, {}, False, groups)
        self.assertEqual(row.attributes()["alarmgruppen_id"], "42")
        self.assertEqual(row.attributes()["alarmgruppe"], "Test-Probe")
        self.assertNotIn("nachricht", row.attributes())
        missing = models.project_notification(notification(), {"alarmgruppenId": 42}, {}, False, groups)
        self.assertIsNone(missing.attributes()["alarmgruppen_id"])

    def test_matched_embedded_group_and_unknown_ids(self):
        groups = project_alarm_groups(profile())
        embedded = models.project_notification(notification(), {}, {"alarmgruppenId": 42}, False, groups)
        self.assertEqual(embedded.alarm_group_name, "Test-Probe")
        unknown = models.project_notification({**notification(), "alarmgruppenId": 77}, {}, {}, False, groups)
        self.assertEqual(unknown.alarm_group_id, "77")
        self.assertEqual(unknown.alarm_group_name, "")
        self.assertEqual(unknown.category, "alarm")


class GroupClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_runtime_fetches_profile_once_and_caches_groups(self):
        session = FakeSession(FakeResponse(profile()), FakeResponse({"items": []}), FakeResponse({"items": []}))
        client = api.LeaClient(session, "PRIVATE_TOKEN")
        first = await client.fetch_snapshot(include_groups=True)
        second = await client.fetch_snapshot(include_groups=True)
        self.assertTrue(first.groups_available)
        self.assertEqual(first.groups, second.groups)
        self.assertEqual([url.rsplit("/", 1)[-1] for _, url, _ in session.requests], ["me", "notifications", "notifications"])
        self.assertTrue(all(method == "GET" for method, _, _ in session.requests))
        self.assertNotIn("PRIVATE", repr(first))

    async def test_failed_group_refresh_keeps_alarm_polling_and_cached_catalogue(self):
        session = FakeSession(FakeResponse(profile()), FakeResponse({"error": "private"}, 500),
                              FakeResponse({"items": [{**notification(), "alarmgruppenId": 42}]}), FakeResponse({"items": []}))
        client = api.LeaClient(session)
        await client.get_profile()
        client._groups_refresh_after = 0
        result = await client.fetch_snapshot(include_groups=True)
        self.assertFalse(result.groups_available)
        self.assertEqual(result.latest.category, "alarm")
        self.assertEqual(result.latest.alarm_group_name, "Test-Probe")
        self.assertEqual(len(result.groups), 1)

    async def test_missing_group_schema_keeps_notification_polling(self):
        session = FakeSession(FakeResponse({"id": "test"}), FakeResponse({"items": []}))
        result = await api.LeaClient(session).fetch_snapshot(include_groups=True)
        self.assertFalse(result.groups_available)
        self.assertEqual(result.notifications, ())

    async def test_auth_and_rate_limits_do_not_fall_through_to_inbox(self):
        for status, error in [(401, api.LeaAuthError), (429, api.LeaRateLimitError)]:
            session = FakeSession(FakeResponse({}, status))
            with self.assertRaises(error):
                await api.LeaClient(session).fetch_snapshot(include_groups=True)
            self.assertEqual(len(session.requests), 1)


if __name__ == "__main__":
    unittest.main()
