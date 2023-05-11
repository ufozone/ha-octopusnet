"""Digital Devices Octopus NET sensor platform."""
from __future__ import annotations

from collections.abc import Callable

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from .const import (
    LOGGER,
    DOMAIN,
    CONF_TUNER_COUNT,
    CONF_STREAM_COUNT,
)
from .coordinator import OctopusNetDataUpdateCoordinator
from .entity import OctopusNetEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Entity,
) -> None:
    """Do setup sensors from a config entry created in the integrations UI."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entity_descriptions = []
    for i in range(1, config_entry.data[CONF_TUNER_COUNT] + 1):
        entity_descriptions.append(
            BinarySensorEntityDescription(
                key=f"tuner_{i}",
                device_class=BinarySensorDeviceClass.RUNNING,
                translation_key="tuner",
            )
        )
    for i in range(1, config_entry.data[CONF_STREAM_COUNT] + 1):
        entity_descriptions.append(
            BinarySensorEntityDescription(
                key=f"stream_{i}",
                device_class=BinarySensorDeviceClass.RUNNING,
                translation_key="stream",
            )
        )

    async_add_entities(
        [
            OctopusNetBinarySensor(
                coordinator=coordinator,
                host=config_entry.data[CONF_HOST],
                entity_description=entity_description,
            )
            for entity_description in entity_descriptions
        ],
        update_before_add=True,
    )


class OctopusNetBinarySensor(OctopusNetEntity, BinarySensorEntity):
    """Representation of a Digital Devices Octopus NET binary sensor."""

    def __init__(
        self,
        coordinator: OctopusNetDataUpdateCoordinator,
        host: str,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator=coordinator,
            host=host,
            entity_type="binary_sensor",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description
