"""Remote platform for vidda_fish."""
from __future__ import annotations

import logging
from typing import Any, Iterable

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_TV_CLIENT_ID,
    CONF_NAME,
    DEFAULT_NAME,
    COMMAND_ALIASES,
)
from .mqtt_client import ViddaMqttClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    mqtt_client: ViddaMqttClient = hass.data[DOMAIN][entry.entry_id]["mqtt"]
    async_add_entities(
        [ViddaFishRemote(mqtt_client, entry.data)], update_before_add=False
    )


class ViddaFishRemote(RemoteEntity):
    _attr_has_entity_name = True
    _attr_name = None
    _attr_should_poll = False
    _attr_is_on = True

    def __init__(self, mqtt_client: ViddaMqttClient, data: dict) -> None:
        self._mqtt = mqtt_client
        self._tv_client_id = data[CONF_TV_CLIENT_ID]

        self._attr_unique_id = f"vidda_fish_{self._tv_client_id}_remote"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._tv_client_id)},
            "name": data.get(CONF_NAME, DEFAULT_NAME),
            "manufacturer": "Hisense",
            "model": "VIDAA",
        }

    async def async_send_command(
        self, command: Iterable[str], **kwargs: Any
    ) -> None:
        for raw in command:
            key = self._resolve(raw)
            if key is None:
                _LOGGER.warning("vidda_fish unknown command: %s", raw)
                continue
            await self.hass.async_add_executor_job(self._mqtt.publish_key, key)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.async_send_command(["KEY_POWER"])

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.async_send_command(["KEY_POWER"])

    @staticmethod
    def _resolve(raw: str) -> str | None:
        if not raw:
            return None
        key = raw.strip()
        if key.startswith("KEY_"):
            return key
        return COMMAND_ALIASES.get(key.lower())
