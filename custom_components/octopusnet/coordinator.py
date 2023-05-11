"""DataUpdateCoordinator for Digital Devices Octopus NET."""
from __future__ import annotations

from datetime import (
    timedelta,
)

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import (
    DOMAIN,
    LOGGER,
    UPDATE_INTERVAL,
)
from .octopusnet import (
    OctopusNetClient,
    OctopusNetClientTimeoutError,
    OctopusNetClientCommunicationError,
)


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
        
        self.client.async_fan_speed()
        self.client.async_tuner_status()
        self.client.async_stream_status()

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.client._session.close()

    async def _async_update_data(self):
        """Update data via library."""
        LOGGER.debug("_async_update_data")
        # TODO

    async def async_reboot(
        self,
    ) -> bool:
        """Send command reboot to device."""
        LOGGER.debug("reboot")
        # TODO

    async def async_epg_scan(
        self,
    ) -> bool:
        """Send command epg_scan to device."""
        LOGGER.debug("epg_scan")
        # TODO
