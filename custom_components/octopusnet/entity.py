"""Digital Devices Octopus NET entity."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    CONF_VERIFY_SSL,
    ATTR_NAME,
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_STATE,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    LOGGER,
    DOMAIN,
    MANUFACTURER,
    ATTR_LAST_PULL,
)
from .coordinator import OctopusNetDataUpdateCoordinator


class OctopusNetEntity(CoordinatorEntity):
    """Digital Devices Octopus NET class."""

    def __init__(
        self,
        coordinator: OctopusNetDataUpdateCoordinator,
        host: str,
        entity_type: str,
        entity_key: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._host = host
        self._entity_type = entity_type
        self._entity_key = entity_key

        if entity_key:
            self._unique_id = slugify(f"{self._host}_{entity_key}")
        else:
            self._unique_id = slugify(f"{self._host}")

        self._available = True
        self._last_pull = None

        self._additional_extra_state_attributes = {}

        self.entity_id = f"{entity_type}.{self._unique_id}"

    def _get_attributes(
        self,
        attr: str,
    ) -> any:
        """Get the mower attributes of the current mower."""
        return self.coordinator.data.get(self._entity_key, {}).get(attr)

    def _update_extra_state_attributes(self) -> None:
        """Update extra attributes."""
        self._additional_extra_state_attributes = {}

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._host

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def device_info(self):
        """Return the device info."""
        return {
            ATTR_IDENTIFIERS: {
                (DOMAIN, self._host)
            },
            ATTR_NAME: self._host,
            ATTR_MANUFACTURER: MANUFACTURER,
        }

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return axtra attributes."""
        _extra_state_attributes = {
            ATTR_LAST_PULL: self._last_pull,
        }
        _extra_state_attributes.update(self._additional_extra_state_attributes)

        return _extra_state_attributes

    async def async_update(self) -> None:
        """Peform async_update."""
        self._update_handler()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_handler()
        self.async_write_ha_state()

    def _update_handler(self) -> None:
        """Handle updated data."""
        LOGGER.debug(self.coordinator.data)
        self._update_extra_state_attributes()
