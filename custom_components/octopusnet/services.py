"""Services Registry for Digital Devices Octopus NET integration."""

from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
)
from homeassistant.const import (
    CONF_DEVICE_ID,
)
from homeassistant.helpers.device_registry import async_get
from homeassistant.helpers.service import (
    verify_domain_control,
)

from .const import (
    DOMAIN,
    SERVICE_REBOOT,
    SERVICE_REBOOT_SCHEMA,
    SERVICE_EPG_SCAN,
    SERVICE_EPG_SCAN_SCHEMA,
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up Digital Devices Octopus NET services."""
    if hass.services.async_services().get(DOMAIN):
        return

    @verify_domain_control(hass, DOMAIN)
    async def async_handle_service(call: ServiceCall) -> None:
        """Call correct Digital Devices Octopus NET service."""
        service = call.service
        data = {**call.data}
        device_ids = data.pop(CONF_DEVICE_ID, [])
        if isinstance(device_ids, str):
            device_ids = [device_ids]
        device_ids = set(device_ids)

        targets = []
        dr = async_get(hass)
        for device_id in device_ids:
            device = dr.async_get(device_id)
            if not device:
                continue
            identifiers = list(device.identifiers)[0]
            if identifiers[0] != DOMAIN:
                continue
            config_entry_id = list(device.config_entries)[0]
            if config_entry_id not in hass.data[DOMAIN]:
                continue
            targets.append(hass.data[DOMAIN][config_entry_id])

        if service == SERVICE_REBOOT:
            await _async_reboot(hass, targets, data)
        elif service == SERVICE_EPG_SCAN:
            await _async_epg_scan(hass, targets, data)

    hass.services.async_register(
        domain=DOMAIN,
        service=SERVICE_REBOOT,
        service_func=async_handle_service,
        schema=SERVICE_REBOOT_SCHEMA
    )
    hass.services.async_register(
        domain=DOMAIN,
        service=SERVICE_EPG_SCAN,
        service_func=async_handle_service,
        schema=SERVICE_EPG_SCAN_SCHEMA
    )

async def _async_reboot(
    hass: HomeAssistant,
    targets: list[any],
    data: dict[str, any],
) -> None:
    """Handle the service call."""
    for coordinator in targets:
        hass.async_create_task(
            coordinator.async_reboot()
        )

async def _async_epg_scan(
    hass: HomeAssistant,
    targets: list[any],
    data: dict[str, any],
) -> None:
    """Handle the service call."""
    for coordinator in targets:
        hass.async_create_task(
            coordinator.async_epg_scan()
        )
