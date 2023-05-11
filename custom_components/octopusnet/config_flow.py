"""Adds config flow for Digital Devices Octopus NET."""
from __future__ import annotations

from copy import deepcopy

from homeassistant.core import (
    callback,
    HomeAssistant,
    HassJob,
)
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
    CONN_CLASS_LOCAL_PUSH,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    CONF_VERIFY_SSL,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import (
    async_create_clientsession,
    async_get_clientsession,
)
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    LOGGER,
    DOMAIN,
)
from .octopusnet import (
    OctopusNetClient,
    OctopusNetClientTimeoutError,
    OctopusNetClientConnectionError,
)

class OctopusNetConfigFlow(ConfigFlow, domain=DOMAIN):
    """Digital Devices Octopus NET config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    data: dict[str, any] | None
    options: dict[str, any] | None

    async def async_step_user(
        self,
        user_input: dict[str, any] | None = None,
    ) -> FlowResult:
        """Invoke when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._async_abort_entries_match(
                {
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input[CONF_PORT],
                }
            )
            session = async_get_clientsession(self.hass, user_input[CONF_VERIFY_SSL])
            octopus = OctopusNetClient(
                host=user_input[CONF_HOST],
                port=user_input[CONF_PORT],
                tls=user_input[CONF_SSL],
                verify_ssl=user_input[CONF_VERIFY_SSL],
                session=session,
            )
            try:
                await octopus.async_fan_speed()
            except OctopusNetClientTimeoutError:
                LOGGER.info(exception)
                errors["base"] = "timeout_connect"
            except OctopusNetClientConnectionError:
                LOGGER.info(exception)
                errors["base"] = "cannot_connect"
            except Exception as exception:
                LOGGER.exception(exception)
                errors["base"] = "unknown"

            if not errors:
                # Input is valid, set data
                self.data = {
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input[CONF_PORT],
                    CONF_SSL: user_input[CONF_SSL],
                    CONF_VERIFY_SSL: user_input[CONF_VERIFY_SSL],
                }
                self.data.update()
                return self.async_create_entry(
                    title=self.data[CONF_HOST],
                    data=self.data,
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST, ""),
                    ): cv.string,
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, 80),
                    ): vol.Coerce(int),
                    vol.Required(
                        CONF_SSL,
                        default=(user_input or {}).get(CONF_SSL, False),
                    ): cv.boolean,
                    vol.Required(
                        CONF_VERIFY_SSL,
                        default=(user_input or {}).get(CONF_VERIFY_SSL, True),
                    ): cv.boolean,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OctopusNetOptionsFlowHandler(config_entry)


class OctopusNetOptionsFlowHandler(OptionsFlow):
    """Handles options flow for the component."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self.data = dict(config_entry.data)

    async def async_step_init(
        self,
        user_input: dict[str, any] = None
    ) -> FlowResult:
        """Manage the options for the custom component."""
        errors: dict[str, str] = {}
        if user_input is not None:
            session = async_get_clientsession(self.hass, user_input[CONF_VERIFY_SSL])
            octopus = OctopusNetClient(
                host=user_input[CONF_HOST],
                port=user_input[CONF_PORT],
                tls=user_input[CONF_SSL],
                verify_ssl=user_input[CONF_VERIFY_SSL],
                session=session,
            )

            if not errors:
                # Input is valid, set data
                self.data = {
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input[CONF_PORT],
                    CONF_SSL: user_input[CONF_SSL],
                    CONF_VERIFY_SSL: user_input[CONF_VERIFY_SSL],
                }
                self.data.update()
                return self.async_create_entry(
                    title=self.data[CONF_HOST],
                    data=self.data,
                )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or self.data).get(CONF_HOST, ""),
                    ): cv.string,
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or self.data).get(CONF_PORT, 80),
                    ): vol.Coerce(int),
                    vol.Required(
                        CONF_SSL,
                        default=(user_input or self.data).get(CONF_SSL, False),
                    ): cv.boolean,
                    vol.Required(
                        CONF_VERIFY_SSL,
                        default=(user_input or self.data).get(CONF_VERIFY_SSL, True),
                    ): cv.boolean,
                }
            ),
            errors=errors,
        )
