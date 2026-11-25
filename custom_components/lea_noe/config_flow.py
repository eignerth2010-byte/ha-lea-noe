"""User-driven SMS login or existing-session login; no background SMS requests."""

from __future__ import annotations

import re
from typing import Any

import probatio as p

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .api import LeaAccessError, LeaAuthError, LeaClient, LeaError, LeaProtocolError, LeaRateLimitError
from .const import (
    CONF_DETAILS, CONF_INTERVAL, CONF_METHOD, CONF_PHONE, CONF_TOKEN,
    DEFAULT_INTERVAL, DOMAIN, MAX_INTERVAL, MIN_INTERVAL, NAME,
)
from .models import normalize_phone, text


def _secret_selector():
    return selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))


def _error_key(error: LeaError) -> str:
    if isinstance(error, LeaRateLimitError):
        return "rate_limited"
    if isinstance(error, LeaAuthError):
        return "invalid_auth"
    if isinstance(error, LeaAccessError):
        return "access_denied"
    if isinstance(error, LeaProtocolError):
        return "invalid_response"
    return "cannot_connect"


class LeaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._phone = ""
        self._cooldown = 60

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LeaOptionsFlow()

    def _auth_client(self) -> LeaClient:
        return LeaClient(async_get_clientsession(self.hass), allow_auth=True)

    async def async_step_user(self, user_input=None):
        return self.async_show_menu(step_id="user", menu_options=["token", "phone"])

    async def async_step_reauth(self, entry_data):
        self._phone = str(entry_data.get(CONF_PHONE, ""))
        return await self.async_step_user()

    async def async_step_reconfigure(self, user_input=None):
        self._phone = str(self._get_reconfigure_entry().data.get(CONF_PHONE, ""))
        return await self.async_step_user()

    async def async_step_phone(self, user_input: dict[str, Any] | None = None):
        errors = {}
        if user_input is not None and user_input.get("confirm_session_change") is not True:
            errors["confirm_session_change"] = "session_change_not_confirmed"
            user_input = None
        if user_input is not None:
            try:
                self._phone = normalize_phone(user_input[CONF_PHONE])
            except (ValueError, TypeError):
                errors[CONF_PHONE] = "invalid_phone"
            else:
                # Do not send another SMS when this exact phone already has an entry.
                if self.source not in {config_entries.SOURCE_REAUTH, config_entries.SOURCE_RECONFIGURE}:
                    if any(entry.data.get(CONF_PHONE) == self._phone for entry in self._async_current_entries()):
                        return self.async_abort(reason="already_configured")
                try:
                    response = await self._auth_client().request_code(self._phone)
                    if response.get("token"):
                        return await self._async_complete(response["token"], "phone")
                except LeaError as err:
                    errors["base"] = _error_key(err)
                    if isinstance(err, LeaRateLimitError):
                        self._cooldown = err.retry_after
                else:
                    return await self.async_step_sms()
        return self.async_show_form(
            step_id="phone", errors=errors,
            data_schema=p.Schema({
                p.Required(CONF_PHONE, default=self._phone): str,
                p.Required("confirm_session_change", default=False): bool,
            }),
            description_placeholders={"seconds": str(self._cooldown)},
        )

    async def async_step_sms(self, user_input: dict[str, Any] | None = None):
        errors = {}
        if not self._phone:
            return await self.async_step_phone()
        if user_input is not None:
            if user_input.get("resend_code"):
                try:
                    response = await self._auth_client().request_code(self._phone)
                    if response.get("token"):
                        return await self._async_complete(response["token"], "phone")
                except LeaError as err:
                    errors["base"] = _error_key(err)
                    if isinstance(err, LeaRateLimitError):
                        self._cooldown = err.retry_after
            else:
                code = str(user_input.get("sms_code", "")).strip()
                if not re.fullmatch(r"[0-9]{5}", code):
                    errors["sms_code"] = "invalid_code"
                else:
                    try:
                        token = await self._auth_client().login(self._phone, code)
                        return await self._async_complete(token, "phone")
                    except LeaError as err:
                        errors["base"] = _error_key(err)
                        if isinstance(err, LeaRateLimitError):
                            self._cooldown = err.retry_after
        return self.async_show_form(
            step_id="sms", errors=errors,
            data_schema=p.Schema({
                p.Optional("sms_code", default=""): _secret_selector(),
                p.Optional("resend_code", default=False): bool,
            }),
            description_placeholders={"phone_suffix": self._phone[-4:], "seconds": str(self._cooldown)},
        )

    async def async_step_token(self, user_input: dict[str, Any] | None = None):
        errors = {}
        if user_input is not None:
            token = str(user_input.get(CONF_TOKEN, "")).strip()
            if not token or len(token) > 16384 or re.search(r"\s", token):
                errors[CONF_TOKEN] = "invalid_auth"
            else:
                try:
                    return await self._async_complete(token, "token")
                except LeaError as err:
                    errors["base"] = _error_key(err)
        return self.async_show_form(
            step_id="token", errors=errors,
            data_schema=p.Schema({p.Required(CONF_TOKEN): _secret_selector()}),
        )

    async def _async_complete(self, token: str, method: str):
        # Validate the account AND read access before retaining any credentials.
        client = LeaClient(async_get_clientsession(self.hass), token)
        profile = await client.get_profile()
        await client.fetch_snapshot()
        await self.async_set_unique_id(text(profile["id"], 128))
        data = {CONF_TOKEN: token, CONF_METHOD: method, CONF_PHONE: self._phone if method == "phone" else ""}
        if self.source in {config_entries.SOURCE_REAUTH, config_entries.SOURCE_RECONFIGURE}:
            self._abort_if_unique_id_mismatch()
            entry = self._get_reauth_entry() if self.source == config_entries.SOURCE_REAUTH else self._get_reconfigure_entry()
            return self.async_update_reload_and_abort(entry, data_updates=data)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=NAME, data=data)


class LeaOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=p.Schema({
                p.Required(CONF_INTERVAL, default=self.config_entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL)):
                    p.All(p.Coerce(int), p.Range(min=MIN_INTERVAL, max=MAX_INTERVAL)),
                p.Required(CONF_DETAILS, default=self.config_entry.options.get(CONF_DETAILS, False)): bool,
            }),
        )

