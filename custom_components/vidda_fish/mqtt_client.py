"""Shared MQTT client for vidda_fish.

整台电视共用一条 MQTT 长连接。首次按键建立，之后复用。
连接断开时自动重连（paho 内置）。
"""
from __future__ import annotations

import logging
import threading
import time

import paho.mqtt.client as mqtt

from .const import CMD_TOPIC_TEMPLATE

_LOGGER = logging.getLogger(__name__)


class ViddaMqttClient:
    """One long-lived MQTT connection per TV."""

    def __init__(
        self,
        host: str,
        port: int,
        tv_client_id: str,
        username: str,
        password: str,
    ) -> None:
        self._host = host
        self._port = port
        self._tv_client_id = tv_client_id
        self._username = username
        self._password = password
        self._topic = CMD_TOPIC_TEMPLATE.format(tv_client_id=tv_client_id)

        self._client: mqtt.Client | None = None
        self._connected = threading.Event()
        self._lock = threading.Lock()

    # ── 连接管理 ─────────────────────────────────────────
    def _build_client(self) -> mqtt.Client:
        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"vidda_fish_{self._tv_client_id[:12]}",
            protocol=mqtt.MQTTv5,
        )
        client.username_pw_set(self._username, self._password)

        def on_connect(c, u, flags, rc, props):
            if rc == 0:
                _LOGGER.info("vidda_fish MQTT connected to %s:%s", self._host, self._port)
                self._connected.set()
            else:
                _LOGGER.warning("vidda_fish MQTT connect failed: %s", rc)
                self._connected.clear()

        def on_disconnect(c, u, flags, rc, props=None):
            _LOGGER.info("vidda_fish MQTT disconnected: %s", rc)
            self._connected.clear()

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect

        # 断线自动重连（1~30 秒退避）
        client.reconnect_delay_set(min_delay=1, max_delay=30)

        return client

    def ensure_connected(self) -> mqtt.Client:
        """Return a connected client. Create if missing; wait if reconnecting."""
        with self._lock:
            if self._client is None:
                self._client = self._build_client()
                self._client.connect_async(self._host, self._port, keepalive=30)
                self._client.loop_start()

            # 等连接就绪（最多 5 秒）
            if not self._connected.wait(timeout=5.0):
                _LOGGER.warning("vidda_fish MQTT not ready within 5s, publishing anyway")

            return self._client

    def publish_key(self, key: str) -> int:
        """Publish a key. Returns MQTT rc."""
        client = self.ensure_connected()
        info = client.publish(self._topic, payload=key, qos=0)
        return info.rc

    def shutdown(self) -> None:
        """Tear down on unload."""
        with self._lock:
            if self._client is not None:
                try:
                    self._client.loop_stop()
                    self._client.disconnect()
                except Exception:  # noqa: BLE001
                    pass
                self._client = None
            self._connected.clear()
