"""Button platform for vidda_fish."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_TV_CLIENT_ID,
    CONF_NAME,
    DEFAULT_NAME,
)
from .mqtt_client import ViddaMqttClient

_LOGGER = logging.getLogger(__name__)

BUTTON_LAYOUT = [
    ("KEY_POWER",      "电源",    "mdi:power"),
    ("KEY_VOLUMEDOWN", "音量-",   "mdi:volume-medium"),
    ("KEY_MUTE",       "静音",    "mdi:volume-off"),
    ("KEY_VOLUMEUP",   "音量+",   "mdi:volume-high"),
    ("KEY_JUBAO",      "AI识图",  "mdi:image-search"),
    ("KEY_UP",         "上",      "mdi:arrow-up"),
    ("KEY_DOWN",       "下",      "mdi:arrow-down"),
    ("KEY_LEFT",       "左",      "mdi:arrow-left"),
    ("KEY_RIGHT",      "右",      "mdi:arrow-right"),
    ("KEY_OK",         "OK",      "mdi:circle-outline"),
    ("KEY_RETURNS",    "返回",    "mdi:arrow-u-left-top"),
    ("KEY_HOME",       "首页",    "mdi:home"),
    ("KEY_MENU",       "菜单",    "mdi:menu"),
    ("KEY_APPS",       "应用",    "mdi:apps"),
    ("KEY_LIVE",       "直播",    "mdi:television"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    mqtt_client: ViddaMqttClient = hass.data[DOMAIN][entry.entry_id]["mqtt"]
    data = entry.data

    async_add_entities(
        [
            ViddaFishButton(mqtt_client, data, key, name, icon)
            for key, name, icon in BUTTON_LAYOUT
        ],
        update_before_add=False,
    )


class ViddaFishButton(ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, mqtt_client, data, key, label, icon) -> None:
        self._mqtt = mqtt_client
        self._key = key
        self._tv_client_id = data[CONF_TV_CLIENT_ID]

        self._attr_unique_id = f"vidda_fish_{self._tv_client_id}_btn_{key}"
        self._attr_name = label
        self._attr_icon = icon
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._tv_client_id)},
            "name": data.get(CONF_NAME, DEFAULT_NAME),
            "manufacturer": "Hisense",
            "model": "VIDDA",
        }

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self._mqtt.publish_key, self._key)
