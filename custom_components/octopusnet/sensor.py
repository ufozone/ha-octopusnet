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
    SensorStateClass,
)
from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
    ATTR_FANSPEED,
    ATTR_TUNER,
    ATTR_STREAM,
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
            translation_key=ATTR_FANSPEED,
            icon="mdi:fan",
            native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        SensorEntityDescription(
            key=ATTR_TEMPERATURE,
            translation_key=ATTR_TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        SensorEntityDescription(
            key=ATTR_TUNER,
            translation_key=ATTR_TUNER,
            icon="mdi:satellite-uplink",
            native_unit_of_measurement=None,
            suggested_unit_of_measurement=None,
            suggested_display_precision=0,
            device_class=None,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        SensorEntityDescription(
            key=ATTR_STREAM,
            translation_key=ATTR_STREAM,
            icon="mdi:monitor-arrow-down",
            native_unit_of_measurement=None,
            suggested_unit_of_measurement=None,
            suggested_display_precision=0,
            device_class=None,
            state_class=SensorStateClass.MEASUREMENT,
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
