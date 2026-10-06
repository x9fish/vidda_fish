"""vidda_fish - local MQTT control for Hisense VIDDA TVs.

Target device: Vidda 85V7N Ultra
Author: x9fish <x9fish@gmail.com>
Repository: https://github.com/x9fish/vidda_fish
Credits: Written by DeepSeek and ChatGPT (web).
License: MIT
"""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_TV_CLIENT_ID,
    CONF_USERNAME,
    CONF_PASSWORD,
)
from .mqtt_client import ViddaMqttClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["remote", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up vidda_fish from a config entry."""
    data = entry.data

    mqtt_client = ViddaMqttClient(
        host=data[CONF_HOST],
        port=data[CONF_PORT],
        tv_client_id=data[CONF_TV_CLIENT_ID],
        username=data[CONF_USERNAME],
        password=data[CONF_PASSWORD],
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "mqtt": mqtt_client,
        "data": data,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        store = hass.data[DOMAIN].pop(entry.entry_id, None)
        if store and (mqtt_client := store.get("mqtt")):
            mqtt_client.shutdown()
    return unload_ok
