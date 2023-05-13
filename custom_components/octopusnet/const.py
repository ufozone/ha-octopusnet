"""Constants for Digital Devices Octopus NET integration."""
from logging import getLogger

import voluptuous as vol
from homeassistant.const import (
    Platform,
    CONF_DEVICE_ID,
)
from homeassistant.helpers import config_validation as cv

LOGGER = getLogger(__package__)

DOMAIN = "octopusnet"
MANUFACTURER = "Digital Devices"

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]

UPDATE_INTERVAL = 120

CONF_TUNER_COUNT = "tuner_count"
CONF_STREAM_COUNT = "stream_count"

ATTR_FANSPEED = "fanspeed"
ATTR_EXTRA_STATE_ATTRIBUTES = "extra_state_attributes"
ATTR_EPG = "epg"
ATTR_TOTAL = "total"
ATTR_EVENTS = "events"
ATTR_TUNER = "tuner"
ATTR_LOCK = "lock"
ATTR_STRENGTH = "strength"
ATTR_SNR = "snr"
ATTR_QUALITY = "quality"
ATTR_LEVEL = "level"
ATTR_STREAM = "stream"
ATTR_INPUT = "input"
ATTR_PACKETS = "packets"
ATTR_BYTES = "bytes"
ATTR_CLIENT = "client"
ATTR_AVAILABLE = "available"
ATTR_LAST_PULL = "last_pull"

SERVICE_REBOOT = "reboot"
SERVICE_REBOOT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
SERVICE_EPG_SCAN = "epg_scan"
SERVICE_EPG_SCAN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
