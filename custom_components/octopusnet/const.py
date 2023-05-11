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
