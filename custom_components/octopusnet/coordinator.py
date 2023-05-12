"""DataUpdateCoordinator for Digital Devices Octopus NET."""
from __future__ import annotations

from datetime import (
    timedelta,
    datetime,
    timezone,
)

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    ATTR_STATE,
    ATTR_TEMPERATURE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import (
    DOMAIN,
    LOGGER,
    UPDATE_INTERVAL,
    ATTR_FANSPEED,
    ATTR_EXTRA_STATE_ATTRIBUTES,
    ATTR_EPG,
    ATTR_TOTAL,
    ATTR_EVENTS,
    ATTR_TUNER,
    ATTR_COUNT,
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
from .octopusnet import OctopusNetClient


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class OctopusNetDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Digital Devices Octopus NET."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: OctopusNetClient,
        update_interval: timedelta = timedelta(seconds=UPDATE_INTERVAL),
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.entry = entry
        self.client = client
        self._last_pull = None

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.client._session.close()

    async def _async_update_data(self):
        """Update data via library."""
        _available = False
        _data = {}
        try:
            _data[ATTR_FANSPEED] = {
                ATTR_STATE: await self.client.async_get_fanspeed(),
            }
            _data[ATTR_TEMPERATURE] = {
                ATTR_STATE: await self.client.async_get_temperature(),
            }
            _epg = await self.client.async_get_epg()
            _epg_state = True if _epg.get("status") == "active" else False
            _data[ATTR_EPG] = {
                ATTR_STATE: _epg_state,
                ATTR_EXTRA_STATE_ATTRIBUTES: {
                    ATTR_TOTAL: _epg.get("total", 0),
                    ATTR_EVENTS: _epg.get("events", 0),
                },
            }
            _tuner_index = 1
            _tuner_total_count = _tuner_total_strength = _tuner_total_snr = _tuner_total_quality = _tuner_total_level = 0
            _tuner_status = await self.client.async_get_tuner_status()
            for _tuner in _tuner_status:
                _tuner_key = f"{ATTR_TUNER}_{_tuner_index}"
                _tuner_state = True if _tuner.get("Status") == "Active" else False
                _tuner_strength = _tuner_snr = _tuner_quality = _tuner_level = 0
                if _tuner_state is True:
                    _tuner_strength = ((int(_tuner.get("Strength", 0)) + 108750) / 1000)
                    _tuner_snr = (int(_tuner.get("SNR", 0)) / 1000)
                    _tuner_quality = _tuner.get("Quality", 0)
                    _tuner_level = _tuner.get("Level", 0)
                    _tuner_total_count += 1
                    _tuner_total_strength += _tuner_strength
                    _tuner_total_snr += _tuner_snr
                    _tuner_total_quality += _tuner_quality
                    _tuner_total_level += _tuner_level

                _data[_tuner_key] = {
                    ATTR_STATE: _tuner_state,
                    ATTR_EXTRA_STATE_ATTRIBUTES: {
                        ATTR_LOCK: _tuner.get("Lock", False),
                        ATTR_STRENGTH: _tuner_strength,
                        ATTR_SNR: _tuner_snr,
                        ATTR_QUALITY: _tuner_quality,
                        ATTR_LEVEL: _tuner_level,
                    }
                }
                _tuner_index = _tuner_index + 1

            if _tuner_total_count > 0:
                _tuner_total_strength = (_tuner_total_strength / _tuner_total_count)
                _tuner_total_snr = (_tuner_total_snr / _tuner_total_count)
                _tuner_total_quality = (_tuner_total_quality / _tuner_total_count)
                _tuner_total_level = (_tuner_total_level / _tuner_total_count)

            _data[ATTR_TUNER] = {
                ATTR_STATE: True if _tuner_total_count > 0 else False,
                ATTR_EXTRA_STATE_ATTRIBUTES: {
                    ATTR_COUNT: _tuner_total_count,
                    ATTR_STRENGTH: _tuner_total_strength,
                    ATTR_SNR: _tuner_total_snr,
                    ATTR_QUALITY: _tuner_total_quality,
                    ATTR_LEVEL: _tuner_total_level,
                },
            }

            _stream_index = 1
            _stream_total_state = False
            _stream_total_input = _stream_total_packets = _stream_total_bytes = _stream_total_clients = 0
            _stream_status = await self.client.async_get_stream_status()
            for _stream in _stream_status:
                _stream_key = f"{ATTR_STREAM}_{_stream_index}"
                _stream_state = True if _stream.get("Status") == "Active" else False
                _stream_input = _stream.get("Input", 0)
                _stream_packets = _stream.get("Packets", 0)
                _stream_bytes = _stream.get("Bytes", 0)
                _stream_client = _stream.get("Client", "")
                if _stream_input:
                    _stream_total_state = True
                _stream_total_input += _stream_input
                _stream_total_packets += _stream_packets
                _stream_total_bytes += _stream_bytes
                if _stream_client:
                    _stream_total_clients += len(_stream_client.split(","))

                _data[_stream_key] = {
                    ATTR_STATE: _stream_state,
                    ATTR_EXTRA_STATE_ATTRIBUTES: {
                        ATTR_INPUT: _stream_input,
                        ATTR_PACKETS: _stream_packets,
                        ATTR_BYTES: _stream_bytes,
                        ATTR_CLIENT: _stream_client,
                    }
                }
                _stream_index = _stream_index + 1

            _data[ATTR_STREAM] = {
                ATTR_STATE: _stream_total_state,
                ATTR_EXTRA_STATE_ATTRIBUTES: {
                    ATTR_INPUT: _stream_total_input,
                    ATTR_PACKETS: _stream_total_packets,
                    ATTR_BYTES: _stream_total_bytes,
                    ATTR_CLIENT: _stream_total_clients,
                },
            }
            self._last_pull = datetime.utcnow().replace(tzinfo=timezone.utc)
            _available = True
        except Exception as exception:
            LOGGER.exception(exception)

        _data.update(
            {
                ATTR_LAST_PULL: self._last_pull,
                ATTR_AVAILABLE: _available,
            }
        )
        return _data

    async def async_reboot(
        self,
    ) -> bool:
        """Send command reboot to device."""
        try:
            return await self.client.async_start_reboot()
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_epg_scan(
        self,
    ) -> bool:
        """Send command epg_scan to device."""
        try:
            return await self.client.async_epg_scan()
        except Exception as exception:
            LOGGER.exception(exception)
