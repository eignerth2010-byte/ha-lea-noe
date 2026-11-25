"""LEA v2 client derived from the supplied, unmodified Android 2.0.0 assets.

Runtime clients can only GET whitelisted resources. The two authentication
POSTs are separately enabled for a user-driven config flow. No receipt,
push-token update, acknowledgement, logout or operational write exists here.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
from typing import Any, TYPE_CHECKING

from .const import API_HOST, INBOX_LIMIT, INCIDENT_LIMIT, VERSION
from .models import Snapshot, project_notification, text

if TYPE_CHECKING:
    from aiohttp import ClientSession


class LeaError(Exception):
    """Sanitized base error: never include response bodies or credentials."""


class LeaAuthError(LeaError):
    pass


class LeaAccessError(LeaError):
    pass


class LeaConnectionError(LeaError):
    pass


class LeaProtocolError(LeaError):
    pass


class LeaRateLimitError(LeaError):
    def __init__(self, retry_after: int = 60) -> None:
        super().__init__("LEA request rate limited")
        self.retry_after = max(1, min(retry_after, 86400))


def retry_seconds(header: str | None, body: Any) -> int:
    try:
        if header:
            if header.strip().isdigit():
                return int(header)
            return max(1, int((parsedate_to_datetime(header) - datetime.now(timezone.utc)).total_seconds()))
        if isinstance(body, dict):
            return int(body.get("erneutMoeglichInSekunden", 60))
    except (ValueError, TypeError, OverflowError):
        pass
    return 60


class LeaClient:
    """Use HA's injected aiohttp session with a fixed HTTPS origin."""

    MAX_BODY = 4 * 1024 * 1024

    def __init__(self, session: ClientSession, token: str | None = None, *, allow_auth: bool = False) -> None:
        self._session = session
        self._token = token
        self._allow_auth = allow_auth

    def __repr__(self) -> str:
        return f"LeaClient(authenticated={bool(self._token)}, allow_auth={self._allow_auth})"

    async def _request(self, method: str, path: str, *, params: dict | None = None, payload: dict | None = None) -> dict:
        allowed_read = method == "GET" and path in {"/me", "/notifications", "/incidents"}
        allowed_auth = self._allow_auth and method == "POST" and path in {"/devices", "/sessions"}
        if not (allowed_read or allowed_auth):
            raise LeaAccessError("This client only permits read access and explicit authentication")
        headers = {"Api-Version": "2", "X-User-Agent": f"HomeAssistant-LEA-ReadOnly/{VERSION}"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        try:
            async with asyncio.timeout(25):
                async with self._session.request(
                    method, API_HOST + path, params=params, json=payload,
                    headers=headers, allow_redirects=False,
                ) as response:
                    raw = bytearray()
                    async for chunk in response.content.iter_chunked(65536):
                        raw.extend(chunk)
                        if len(raw) > self.MAX_BODY:
                            raise LeaProtocolError("LEA response exceeds the size limit")
                    try:
                        body = json.loads(raw) if raw else None
                    except (ValueError, UnicodeError):
                        body = None
                    status = response.status
                    if status == 429:
                        raise LeaRateLimitError(retry_seconds(response.headers.get("Retry-After"), body))
                    if status == 401 or (path == "/sessions" and status == 400):
                        raise LeaAuthError("LEA credentials or SMS code were rejected")
                    if status == 403:
                        raise LeaAccessError("LEA access denied")
                    if status >= 500:
                        raise LeaConnectionError("LEA server unavailable")
                    if not 200 <= status < 300:
                        raise LeaProtocolError(f"LEA HTTP status {status}")
                    if not isinstance(body, dict):
                        raise LeaProtocolError("LEA returned an unexpected response structure")
                    if body.get("Fehler") or body.get("error"):
                        raise LeaProtocolError("LEA returned an application error")
                    return body
        except LeaError:
            raise
        except Exception:
            # Isolate transport/decoder errors; aiohttp exceptions may contain
            # a URL, headers or a response. Never expose their original text.
            raise LeaConnectionError("LEA network request failed") from None

    async def request_code(self, phone: str) -> dict:
        """Explicit SMS action, using the app's documented-in-code iOS no-push path."""
        response = await self._request("POST", "/devices", payload={
            "telefonnummer": phone, "platform": "ios", "pushNotificationToken": "",
        })
        if not (response.get("token") or response.get("message") or response.get("Nachricht")):
            raise LeaProtocolError("LEA did not confirm the SMS request")
        return response

    async def login(self, phone: str, code: str) -> str:
        response = await self._request("POST", "/sessions", payload={
            "telefonnummer": phone, "smsToken": code,
            "pushNotificationToken": None, "platform": "ios",
        })
        token = response.get("token")
        if not isinstance(token, str) or not token.strip():
            raise LeaProtocolError("LEA did not return a session token")
        return token.strip()

    async def get_profile(self) -> dict:
        response = await self._request("GET", "/me")
        if not text(response.get("id"), 128):
            raise LeaProtocolError("LEA profile has no identity")
        return response

    @staticmethod
    def _items(response: dict) -> list[dict]:
        rows = response.get("items")
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise LeaProtocolError("LEA returned an invalid item list")
        return rows

    async def fetch_snapshot(self, *, include_details: bool = False) -> Snapshot:
        inbox = self._items(await self._request("GET", "/notifications", params={"limit": INBOX_LIMIT}))
        # Empty personal inbox does not require an incident request.
        incidents = self._items(await self._request("GET", "/incidents", params={
            "limit": INCIDENT_LIMIT, "offset": 0, "with": "notifications",
        })) if inbox else []
        by_number = {text(row.get("einsatznummer"), 128): row for row in incidents}
        notifications = []
        seen: set[str] = set()
        for row in inbox:
            incident = by_number.get(text(row.get("einsatznummer"), 128), {})
            embedded_rows = incident.get("notifications", [])
            if not isinstance(embedded_rows, list):
                raise LeaProtocolError("LEA returned invalid embedded notifications")
            embedded = next((item for item in embedded_rows if isinstance(item, dict) and (
                (row.get("uuid") and item.get("uuid") == row["uuid"])
                or (row.get("benachrichtigungId") is not None and str(item.get("benachrichtigungId")) == str(row["benachrichtigungId"]))
            )), {})
            notification = project_notification(row, incident, embedded, include_details)
            if notification is None:
                raise LeaProtocolError("LEA personal notification has no stable identifier")
            if notification.identifier not in seen:
                notifications.append(notification)
                seen.add(notification.identifier)
        # Stable sort preserves inbox order when timestamps are absent/equal.
        notifications.sort(key=lambda item: item.timestamp or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        return Snapshot(tuple(notifications), datetime.now(timezone.utc))
