"""Digital Devices Octopus NET integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    CONF_VERIFY_SSL,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    PLATFORMS,
)
from .octopusnet import (
    OctopusNetClient,
)
from .services import async_setup_services
from .coordinator import OctopusNetDataUpdateCoordinator


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Digital Devices Octopus NET component."""
    hass.data.setdefault(DOMAIN, {})

    await async_setup_services(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator = OctopusNetDataUpdateCoordinator(
        hass=hass,
        config_entry=config_entry,
        client=OctopusNetClient(
            host=config_entry.data[CONF_HOST],
            port=config_entry.data[CONF_PORT],
            tls=config_entry.data[CONF_SSL],
            verify_ssl=config_entry.data[CONF_VERIFY_SSL],
            session=async_get_clientsession(hass),
        ),
    )
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS):
        # Remove config entry from domain.
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
