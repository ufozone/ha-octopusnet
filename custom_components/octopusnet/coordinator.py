"""DataUpdateCoordinator for Digital Devices Octopus NET."""
from __future__ import annotations

import asyncio

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_SSL,
    CONF_VERIFY_SSL,
    ATTR_STATE,
    ATTR_TEMPERATURE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
import homeassistant.util.dt as dt_util

from .const import (
    DOMAIN,
    LOGGER,
    UPDATE_INTERVAL,
    ATTR_UPDATE,
    ATTR_FANSPEED,
    ATTR_EXTRA_STATE_ATTRIBUTES,
    ATTR_EPG,
    ATTR_EPG_SCAN,
    ATTR_REBOOT,
    ATTR_TOTAL,
    ATTR_EVENTS,
    ATTR_TUNER,
    ATTR_LOCK,
    ATTR_STRENGTH,
    ATTR_SNR,
    ATTR_QUALITY,
    ATTR_LEVEL,
    ATTR_STREAM,
    ATTR_INPUT,
    ATTR_PACKETS,
    ATTR_BYTES,
    ATTR_CLIENT,
    ATTR_AVAILABLE,
    ATTR_LAST_PULL,
)
from .api import (
    OctopusNetApiClient,
    OctopusNetApiError,
)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class OctopusNetDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Digital Devices Octopus NET."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        update_interval: timedelta = timedelta(seconds=UPDATE_INTERVAL),
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.config_entry = config_entry
        self.client = OctopusNetApiClient(
            host=config_entry.data.get(CONF_HOST),
            username=config_entry.data.get(CONF_USERNAME, ""),
            password=config_entry.data.get(CONF_PASSWORD, ""),
            port=config_entry.data.get(CONF_PORT),
            tls=config_entry.data.get(CONF_SSL),
            verify_ssl=config_entry.data.get(CONF_VERIFY_SSL),
            session=async_get_clientsession(hass),
        )
        self.data = {}
        self._loop = asyncio.get_event_loop()
        self._scheduled_update_listeners: asyncio.TimerHandle | None = None

    async def initialize(self) -> None:
        """Set up a Octopus NET instance."""

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.client._session.close()

    async def _async_update_data(self):
        """Update data via library."""
        self.data = {
            ATTR_UPDATE: {
                ATTR_AVAILABLE: True,
            },
            ATTR_FANSPEED: {
                ATTR_STATE: None,
                ATTR_AVAILABLE: False,
            },
            ATTR_TEMPERATURE: {
                ATTR_STATE: None,
                ATTR_AVAILABLE: False,
            },
            ATTR_EPG: {
                ATTR_STATE: None,
                ATTR_EXTRA_STATE_ATTRIBUTES: {
                    ATTR_TOTAL: None,
                    ATTR_EVENTS: None,
                },
                ATTR_AVAILABLE: False,
            },
            ATTR_EPG_SCAN: {
                ATTR_AVAILABLE: False,
            },
            ATTR_REBOOT: {
                ATTR_AVAILABLE: False,
            },
            ATTR_TUNER: {
                ATTR_STATE: None,
                ATTR_EXTRA_STATE_ATTRIBUTES: {
                    ATTR_LOCK: None,
                    ATTR_STRENGTH: None,
                    ATTR_SNR: None,
                    ATTR_QUALITY: None,
                    ATTR_LEVEL: None,
                },
                ATTR_AVAILABLE: False,
            },
            ATTR_STREAM: {
                ATTR_STATE: None,
                ATTR_EXTRA_STATE_ATTRIBUTES: {
                    ATTR_INPUT: None,
                    ATTR_PACKETS: None,
                    ATTR_BYTES: None,
                    ATTR_CLIENT: None,
                },
                ATTR_AVAILABLE: False,
            },
            ATTR_LAST_PULL: None,
            ATTR_AVAILABLE: False,
        }

        try:
            self.data.update(
                {
                    ATTR_FANSPEED: {
                        ATTR_STATE: await self.client.async_get_fanspeed(),
                        ATTR_AVAILABLE: True,
                    },
                }
            )
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

        try:
            self.data.update(
                {
                    ATTR_TEMPERATURE: {
                        ATTR_STATE: await self.client.async_get_temperature(),
                        ATTR_AVAILABLE: True,
                    },
                    ATTR_REBOOT: {
                        ATTR_AVAILABLE: True,
                    },
                }
            )
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

        try:
            _epg = await self.client.async_get_epg()
            _epg_state = _epg.get("status") == "active"

            self.data.update(
                {
                    ATTR_EPG: {
                        ATTR_STATE: _epg_state,
                        ATTR_EXTRA_STATE_ATTRIBUTES: {
                            ATTR_TOTAL: _epg.get("total", 0),
                            ATTR_EVENTS: _epg.get("events", 0),
                        },
                        ATTR_AVAILABLE: True,
                    },
                    ATTR_EPG_SCAN: {
                        ATTR_AVAILABLE: True,
                    },
                }
            )
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

        try:
            _tuner_index = 1
            _tuner_total_lock = False
            _tuner_total_count = _tuner_total_strength = _tuner_total_snr = _tuner_total_quality = _tuner_total_level = 0
            _tuner_status = await self.client.async_get_tuner_status()
            for _tuner in _tuner_status:
                _tuner_key = f"{ATTR_TUNER}_{_tuner_index}"
                _tuner_state = _tuner.get("Status") == "Active"
                _tuner_lock = _tuner.get("Lock", False)
                _tuner_strength = _tuner_snr = _tuner_quality = _tuner_level = 0
                if _tuner_state:
                    if _tuner_lock:
                        _tuner_total_lock = True
                    _tuner_strength = ((int(_tuner.get("Strength", 0)) + 108750) / 1000)
                    _tuner_snr = (int(_tuner.get("SNR", 0)) / 1000)
                    _tuner_quality = _tuner.get("Quality", 0)
                    _tuner_level = _tuner.get("Level", 0)
                    _tuner_total_count += 1
                    _tuner_total_strength += _tuner_strength
                    _tuner_total_snr += _tuner_snr
                    _tuner_total_quality += _tuner_quality
                    _tuner_total_level += _tuner_level

                self.data.update(
                    {
                        _tuner_key: {
                            ATTR_STATE: _tuner_state,
                            ATTR_EXTRA_STATE_ATTRIBUTES: {
                                ATTR_LOCK: _tuner_lock,
                                ATTR_STRENGTH: _tuner_strength,
                                ATTR_SNR: _tuner_snr,
                                ATTR_QUALITY: _tuner_quality,
                                ATTR_LEVEL: _tuner_level,
                            },
                            ATTR_AVAILABLE: True,
                        },
                    }
                )
                _tuner_index = _tuner_index + 1

            if _tuner_total_count > 0:
                _tuner_total_strength = (_tuner_total_strength / _tuner_total_count)
                _tuner_total_snr = (_tuner_total_snr / _tuner_total_count)
                _tuner_total_quality = (_tuner_total_quality / _tuner_total_count)
                _tuner_total_level = (_tuner_total_level / _tuner_total_count)

            self.data.update(
                {
                    ATTR_TUNER: {
                        ATTR_STATE: _tuner_total_count,
                        ATTR_EXTRA_STATE_ATTRIBUTES: {
                            ATTR_LOCK: _tuner_total_lock,
                            ATTR_STRENGTH: _tuner_total_strength,
                            ATTR_SNR: _tuner_total_snr,
                            ATTR_QUALITY: _tuner_total_quality,
                            ATTR_LEVEL: _tuner_total_level,
                        },
                        ATTR_AVAILABLE: True,
                    },
                }
            )
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

        try:
            _stream_index = 1
            _stream_total_state = False
            _stream_total_input = _stream_total_packets = _stream_total_bytes = 0
            _stream_total_clients = []
            _stream_status = await self.client.async_get_stream_status()
            for _stream in _stream_status:
                _stream_key = f"{ATTR_STREAM}_{_stream_index}"
                _stream_state = _stream.get("Status") == "Active"
                _stream_input = _stream.get("Input", 0)
                _stream_packets = _stream.get("Packets", 0)
                _stream_bytes = _stream.get("Bytes", 0)
                _stream_client = _stream.get("Client", "")
                if _stream_state:
                    _stream_total_state = True
                _stream_total_input += _stream_input
                _stream_total_packets += _stream_packets
                _stream_total_bytes += _stream_bytes
                if _stream_client:
                    _stream_total_clients = _stream_total_clients + _stream_client.split(" ")

                self.data.update(
                    {
                        _stream_key: {
                            ATTR_STATE: _stream_state,
                            ATTR_EXTRA_STATE_ATTRIBUTES: {
                                ATTR_INPUT: _stream_input,
                                ATTR_PACKETS: _stream_packets,
                                ATTR_BYTES: _stream_bytes,
                                ATTR_CLIENT: _stream_client,
                            },
                            ATTR_AVAILABLE: True,
                        },
                    }
                )
                _stream_index = _stream_index + 1

            self.data.update(
                {
                    ATTR_STREAM: {
                        ATTR_STATE: len(_stream_total_clients),
                        ATTR_EXTRA_STATE_ATTRIBUTES: {
                            ATTR_INPUT: _stream_total_input,
                            ATTR_PACKETS: _stream_total_packets,
                            ATTR_BYTES: _stream_total_bytes,
                            ATTR_CLIENT: " ".join([str(v) for v in _stream_total_clients]),
                        },
                        ATTR_AVAILABLE: True,
                    },
                }
            )
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

        self.data.update(
            {
                ATTR_LAST_PULL: dt_util.now(),
            }
        )
        return self.data

    async def _async_update_listeners(self) -> None:
        """Schedule update all registered listeners after 1 second."""
        if self._scheduled_update_listeners:
            self._scheduled_update_listeners.cancel()

        self._scheduled_update_listeners = self.hass.loop.call_later(
            1,
            lambda: self.async_update_listeners(),
        )

    async def async_update_data(
        self,
    ) -> None:
        """Update data."""
        try:
            await self._async_update_data()

            self.hass.async_create_task(
                self._async_update_listeners()
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_reboot(
        self,
    ) -> bool:
        """Send command reboot to device."""
        try:
            return await self.client.async_start_reboot()
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_epg_scan(
        self,
    ) -> bool:
        """Send command epg_scan to device."""
        try:
            return await self.client.async_epg_scan()
        except OctopusNetApiError as exception:
            LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)
