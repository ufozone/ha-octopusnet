"""Digital Devices Octopus NET sensor platform."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
    REVOLUTIONS_PER_MINUTE,
    UnitOfTemperature,
    ATTR_TEMPERATURE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
    ATTR_FANSPEED,
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
            key=ATTR_FANSPEED,
            device_class=SensorDeviceClass.SPEED,
            native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            translation_key=ATTR_FANSPEED,
        ),
        SensorEntityDescription(
            key=ATTR_TEMPERATURE,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key=ATTR_TEMPERATURE,
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

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self._get_state()
