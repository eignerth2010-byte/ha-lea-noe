"""Authenticated, cached LEA view and a sidebar panel. No upstream writes."""

from pathlib import Path
import probatio as p

from homeassistant.components import frontend, panel_custom, websocket_api
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, VERSION
from .sounds import SOUNDS

PANEL_PATH = "lea-noe"
STATIC_PATH = "/lea-noe-static"


async def async_setup_frontend(hass: HomeAssistant) -> None:
    data = hass.data.setdefault(DOMAIN, {"entries": {}, "panel_owned": False})
    if data.get("frontend_ready"):
        return
    await hass.http.async_register_static_paths([
        StaticPathConfig(STATIC_PATH, str(Path(__file__).parent / "frontend"), True),
    ])
    websocket_api.async_register_command(hass, websocket_notifications)
    data["frontend_ready"] = True


async def async_add_entry_panel(hass: HomeAssistant, entry_id: str, coordinator) -> None:
    data = hass.data[DOMAIN]
    data["entries"][entry_id] = coordinator
    # Respect a dashboard or panel which the user already owns at this path.
    if frontend.async_panel_exists(hass, PANEL_PATH):
        return
    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=PANEL_PATH,
        webcomponent_name="lea-noe-panel",
        sidebar_title="LEA",
        sidebar_icon="mdi:alarm-light",
        module_url=f"{STATIC_PATH}/lea-card.js?v={VERSION}",
        require_admin=True,
        config={"integration": DOMAIN},
    )
    data["panel_owned"] = True


@callback
def async_remove_entry_panel(hass: HomeAssistant, entry_id: str) -> None:
    data = hass.data.get(DOMAIN, {})
    data.get("entries", {}).pop(entry_id, None)
    if not data.get("entries") and data.get("panel_owned"):
        frontend.async_remove_panel(hass, PANEL_PATH)
        data["panel_owned"] = False


@websocket_api.websocket_command({p.Required("type"): "lea_noe/get_notifications"})
@websocket_api.require_admin
@callback
def websocket_notifications(hass: HomeAssistant, connection, msg: dict) -> None:
    """Return only projected coordinator data to an authenticated HA admin."""
    accounts = []
    registry = er.async_get(hass)
    for entry_id, coordinator in hass.data.get(DOMAIN, {}).get("entries", {}).items():
        snapshot = coordinator.data
        accounts.append({
            "entry_id": entry_id,
            "title": coordinator.entry.title,
            "available": coordinator.last_update_success,
            "include_details": coordinator.include_details,
            "fetched_at": snapshot.fetched_at.isoformat() if snapshot else None,
            "notifications": [item.attributes(coordinator.include_details) for item in snapshot.notifications] if snapshot else [],
            "audio": {
                **(coordinator.audio.settings if coordinator.audio else {}),
                "test_entity": registry.async_get_entity_id("button", DOMAIN, f"{coordinator.entry.unique_id}_test_alarm_sound"),
                "stop_entity": registry.async_get_entity_id("button", DOMAIN, f"{coordinator.entry.unique_id}_stop_alarm_sound"),
            },
        })
    connection.send_result(msg["id"], {"version": VERSION, "accounts": accounts, "sounds": list(SOUNDS.values())})

