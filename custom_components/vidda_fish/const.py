"""Constants for vidda_fish."""

DOMAIN = "vidda_fish"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_TV_CLIENT_ID = "tv_client_id"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_NAME = "name"

DEFAULT_HOST = ""
DEFAULT_PORT = 36669
DEFAULT_USERNAME = "hisenseservice"
DEFAULT_PASSWORD = "multimqttservice"
DEFAULT_NAME = "Vidda TV"

CMD_TOPIC_TEMPLATE = (
    "/remoteapp/tv/hiservice_cmd/{tv_client_id}/actions/sendkey"
)

SUPPORTED_KEYS = [
    "KEY_POWER",
    "KEY_VOLUMEUP",
    "KEY_VOLUMEDOWN",
    "KEY_MUTE",
    "KEY_UP",
    "KEY_DOWN",
    "KEY_LEFT",
    "KEY_RIGHT",
    "KEY_OK",
    "KEY_RETURNS",
    "KEY_HOME",
    "KEY_MENU",
    "KEY_APPS",
    "KEY_LIVE",
    "KEY_JUBAO",
]

COMMAND_ALIASES = {
    "power": "KEY_POWER",
    "power_on": "KEY_POWER",
    "power_off": "KEY_POWER",
    "volume_up": "KEY_VOLUMEUP",
    "volume_down": "KEY_VOLUMEDOWN",
    "mute": "KEY_MUTE",
    "up": "KEY_UP",
    "down": "KEY_DOWN",
    "left": "KEY_LEFT",
    "right": "KEY_RIGHT",
    "ok": "KEY_OK",
    "select": "KEY_OK",
    "back": "KEY_RETURNS",
    "return": "KEY_RETURNS",
    "home": "KEY_HOME",
    "menu": "KEY_MENU",
    "apps": "KEY_APPS",
    "live": "KEY_LIVE",
    "hdmi": "KEY_LIVE",
    "jubao": "KEY_JUBAO",
    "ai": "KEY_JUBAO",
}


# -- meta --
__version__ = "1.0.1"
AUTHOR = "x9fish"
AUTHOR_EMAIL = "x9fish@gmail.com"
GITHUB = "https://github.com/x9fish/vidda_fish"
DESCRIPTION = "HAOS control for Vidda 85V7N Ultra TV via local MQTT."
CREDITS = "Written by DeepSeek and ChatGPT (web). Code belongs to the internet."
