"""Config flow for vidda_fish."""
from __future__ import annotations

import asyncio
import logging
import re
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_TV_CLIENT_ID,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_NAME,
    DEFAULT_PORT,
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
    DEFAULT_NAME,
)

_LOGGER = logging.getLogger(__name__)

TV_CLIENT_ID_RE = re.compile(r"^[0-9A-Fa-f]{32}$")


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_TV_CLIENT_ID): str,
        vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): str,
        vol.Optional(CONF_PASSWORD, default=DEFAULT_PASSWORD): str,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
    }
)


async def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate TCP connection to the MQTT broker."""
    host = data[CONF_HOST]
    port = data[CONF_PORT]
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=5.0
        )
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:  # noqa: BLE001
            pass
    except Exception as err:  # noqa: BLE001
        _LOGGER.error("Cannot connect to %s:%s — %s", host, port, err)
        raise CannotConnect from err


class ViddaFishConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for vidda_fish."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            cid = (user_input.get(CONF_TV_CLIENT_ID) or "").strip()
            if not TV_CLIENT_ID_RE.match(cid):
                errors[CONF_TV_CLIENT_ID] = "tv_client_id_invalid"
            else:
                user_input[CONF_TV_CLIENT_ID] = cid.upper()

                await self.async_set_unique_id(user_input[CONF_TV_CLIENT_ID])
                self._abort_if_unique_id_configured()

                try:
                    await _validate_input(self.hass, user_input)
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                except Exception:  # noqa: BLE001
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"
                else:
                    return self.async_create_entry(
                        title=user_input.get(CONF_NAME, DEFAULT_NAME),
                        data=user_input,
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
