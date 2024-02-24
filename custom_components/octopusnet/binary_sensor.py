"""Digital Devices Octopus NET binary sensor platform."""
from __future__ import annotations

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
from homeassistant.helpers.entity import (
    Entity,
    EntityCategory,
)

from .const import (
    DOMAIN,
    CONF_TUNER_COUNT,
    CONF_STREAM_COUNT,
    ATTR_EPG,
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
    """Do setup binary sensors from a config entry created in the integrations UI."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entity_descriptions = [
        BinarySensorEntityDescription(
            key=ATTR_EPG,
            translation_key=ATTR_EPG,
            device_class=BinarySensorDeviceClass.RUNNING,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ]
    for i in range(1, config_entry.data[CONF_TUNER_COUNT] + 1):
        entity_descriptions.append(
            BinarySensorEntityDescription(
                key=f"{ATTR_TUNER}_{i}",
                name=f"Tuner {i}",
                translation_key=ATTR_TUNER,
                device_class=BinarySensorDeviceClass.RUNNING,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
            )
        )
    for i in range(1, config_entry.data[CONF_STREAM_COUNT] + 1):
        entity_descriptions.append(
            BinarySensorEntityDescription(
                key=f"{ATTR_STREAM}_{i}",
                name=f"Stream {i}",
                translation_key=ATTR_STREAM,
                device_class=BinarySensorDeviceClass.RUNNING,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
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
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor class."""
        super().__init__(
            coordinator=coordinator,
            host=host,
            entity_type="binary_sensor",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self._get_state()
