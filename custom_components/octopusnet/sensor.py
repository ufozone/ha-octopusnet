"""Digital Devices Octopus NET sensor platform."""
from __future__ import annotations

from collections.abc import Callable

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
    REVOLUTIONS_PER_MINUTE,
    UnitOfTemperature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
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
    entity_descriptions = [
        SensorEntityDescription(
            key="fanspeed",
            device_class=SensorDeviceClass.SPEED,
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            translation_key="fanspeed",
        ),
        SensorEntityDescription(
            key="temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
    ]

    async_add_entities(
        [
            OctopusNetSensor(
                coordinator=coordinator,
                host=config_entry.data[CONF_HOST],
                entity_description=entity_description,
            )
            for entity_description in entity_descriptions
        ],
        update_before_add=True,
    )


class OctopusNetSensor(OctopusNetEntity, SensorEntity):
    """Representation of a Digital Devices Octopus NET sensor."""

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
            entity_type="sensor",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description
