"""Digital Devices Octopus NET button platform."""
from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.helpers.entity import (
    Entity,
    EntityCategory,
)

from .const import (
    ATTR_UPDATE,
    ATTR_EPG_SCAN,
    ATTR_REBOOT,
)
from .coordinator import OctopusNetDataUpdateCoordinator
from .entity import OctopusNetEntity


@dataclass
class OctopusNetButtonDescriptionMixin:
    """Mixin to describe a Digital Devices Octopus NET button entity."""

    press_action: Callable[[OctopusNetDataUpdateCoordinator], Coroutine]


@dataclass
class OctopusNetButtonDescription(
    ButtonEntityDescription,
    OctopusNetButtonDescriptionMixin,
):
    """Digital Devices Octopus NET button description."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Entity,
) -> None:
    """Do setup buttons from a config entry created in the integrations UI."""
    coordinator = config_entry.runtime_data
    entity_descriptions = [
        OctopusNetButtonDescription(
            key=ATTR_UPDATE,
            translation_key=ATTR_UPDATE,
            device_class=ButtonDeviceClass.UPDATE,
            entity_category=EntityCategory.DIAGNOSTIC,
            press_action=lambda coordinator: coordinator.async_update_data(),
        ),
        OctopusNetButtonDescription(
            key=ATTR_REBOOT,
            translation_key=ATTR_REBOOT,
            device_class=ButtonDeviceClass.RESTART,
            entity_category=EntityCategory.CONFIG,
            press_action=lambda coordinator: coordinator.async_reboot(),
        ),
        OctopusNetButtonDescription(
            key=ATTR_EPG_SCAN,
            icon="mdi:cloud-search",
            translation_key=ATTR_EPG_SCAN,
            press_action=lambda coordinator: coordinator.async_epg_scan(),
        ),
    ]

    async_add_entities(
        [
            OctopusNetButton(
                coordinator=coordinator,
                host=config_entry.data[CONF_HOST],
                entity_description=entity_description,
            )
            for entity_description in entity_descriptions
        ],
        update_before_add=True,
    )


class OctopusNetButton(OctopusNetEntity, ButtonEntity):
    """Representation of a Digital Devices Octopus NET button."""

    def __init__(
        self,
        coordinator: OctopusNetDataUpdateCoordinator,
        host: str,
        entity_description: OctopusNetButtonDescription,
    ) -> None:
        """Initialize the button class."""
        super().__init__(
            coordinator=coordinator,
            host=host,
            entity_type="button",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description

    async def async_press(self) -> None:
        """Trigger the button action."""
        await self.entity_description.press_action(self.coordinator)
