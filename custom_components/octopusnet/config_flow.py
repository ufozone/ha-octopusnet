"""Adds config flow for Digital Devices Octopus NET."""
from __future__ import annotations

from homeassistant.config_entries import (
    ConfigFlow,
    CONN_CLASS_LOCAL_PUSH,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    CONF_VERIFY_SSL,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import (
    async_create_clientsession,
)
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    LOGGER,
    DOMAIN,
    CONF_TUNER_COUNT,
    CONF_STREAM_COUNT,
)
from .octopusnet import (
    OctopusNetClient,
    OctopusNetClientTimeoutError,
    OctopusNetClientCommunicationError,
)

class OctopusNetConfigFlow(ConfigFlow, domain=DOMAIN):
    """Digital Devices Octopus NET config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        """Initialize the Digital Devices Octopus NET flow."""
        self.data: dict[str, any] | None = None
        self.options: dict[str, any] | None = None

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
            try:
                session = async_create_clientsession(self.hass, user_input[CONF_VERIFY_SSL])
                octopus = OctopusNetClient(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    tls=user_input[CONF_SSL],
                    verify_ssl=user_input[CONF_VERIFY_SSL],
                    session=session,
                )
                _tuners = await octopus.async_get_tuner_status()
                _streams = await octopus.async_get_stream_status()
            except OctopusNetClientTimeoutError as exception:
                LOGGER.info(exception)
                errors["base"] = "timeout_connect"
            except OctopusNetClientCommunicationError as exception:
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
                    CONF_TUNER_COUNT: len(_tuners),
                    CONF_STREAM_COUNT: len(_streams),
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
