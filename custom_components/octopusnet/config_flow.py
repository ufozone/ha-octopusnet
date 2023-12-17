"""Adds config flow for Digital Devices Octopus NET."""
from __future__ import annotations

from homeassistant.config_entries import (
    ConfigFlow,
    CONN_CLASS_LOCAL_PUSH,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
    CONF_SSL,
    CONF_VERIFY_SSL,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import (
    selector,
)
from homeassistant.helpers.aiohttp_client import (
    async_create_clientsession,
)
import voluptuous as vol

from .const import (
    LOGGER,
    DOMAIN,
    CONF_TUNER_COUNT,
    CONF_STREAM_COUNT,
)
from .api import (
    OctopusNetApiClient,
    OctopusNetApiTimeoutError,
    OctopusNetApiCommunicationError,
    OctopusNetApiAuthenticationError,
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
                    CONF_HOST: user_input.get(CONF_HOST),
                    CONF_PORT: user_input.get(CONF_PORT),
                }
            )
            try:
                client = OctopusNetApiClient(
                    host=user_input.get(CONF_HOST),
                    username=user_input.get(CONF_USERNAME),
                    password=user_input.get(CONF_PASSWORD),
                    port=int(user_input.get(CONF_PORT)),
                    tls=user_input.get(CONF_SSL, False),
                    verify_ssl=user_input.get(CONF_VERIFY_SSL, False),
                    session=async_create_clientsession(self.hass, user_input.get(CONF_VERIFY_SSL, False)),
                )
                _tuners = await client.async_get_tuner_status()
                _streams = await client.async_get_stream_status()
            except OctopusNetApiAuthenticationError:
                errors["base"] = "invalid_auth"
            except OctopusNetApiTimeoutError as exception:
                LOGGER.info(exception)
                errors["base"] = "timeout_connect"
            except OctopusNetApiCommunicationError as exception:
                LOGGER.info(exception)
                errors["base"] = "cannot_connect"
            except Exception as exception:
                LOGGER.exception(exception)
                errors["base"] = "unknown"

            if not errors:
                # Input is valid, set data
                self.data = {
                    CONF_HOST: user_input.get(CONF_HOST),
                    CONF_USERNAME: user_input.get(CONF_USERNAME),
                    CONF_PASSWORD: user_input.get(CONF_PASSWORD),
                    CONF_PORT: int(user_input.get(CONF_PORT)),
                    CONF_SSL: user_input.get(CONF_SSL, False),
                    CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL, False),
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
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_PASSWORD,
                        default=(user_input or {}).get(CONF_PASSWORD, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, 80),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            mode=selector.NumberSelectorMode.BOX,
                            min=1,
                            max=65535,
                        )
                    ),
                    vol.Optional(
                        CONF_SSL,
                        default=(user_input or {}).get(CONF_SSL, False),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        CONF_VERIFY_SSL,
                        default=(user_input or {}).get(CONF_VERIFY_SSL, True),
                    ): selector.BooleanSelector(),
                }
            ),
            errors=errors,
        )
