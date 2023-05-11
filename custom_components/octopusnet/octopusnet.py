"""Digital Devices Octopus NET Client."""
from __future__ import annotations

import asyncio
import socket
import aiohttp
import async_timeout

from homeassistant.helpers.aiohttp_client import HassClientResponse

from .const import LOGGER


class OctopusNetClientError(Exception):
    """Exception to indicate a general client error."""


class OctopusNetClientTimeoutError(OctopusNetClientError):
    """Exception to indicate a timeout error."""


class OctopusNetClientConnectionError(OctopusNetClientError):
    """Exception to indicate a communication error."""


class OctopusNetClientAuthenticationError(OctopusNetClientError):
    """Exception to indicate an authentication error."""


class OctopusNetClient:
    """Octopus NET Client."""

    def __init__(
        self,
        host: str,
        port: int,
        tls: bool,
        verify_ssl: bool,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize."""
        self._host = host
        self._port = port
        self._tls = tls
        self._verify_ssl = verify_ssl
        self._session = session
        if self._tls:
            self._endpoint = f"https://{self._host}:{self._port}"
        else:
            self._endpoint = f"http://{self._host}:{self._port}"

    async def _async_request_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> HassClientResponse:
        """Get information from the device."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise OctopusNetClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return response
        except asyncio.TimeoutError as exception:
            raise OctopusNetClientTimeoutError(
                "Timeout error fetching information"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise OctopusNetClientConnectionError(
                "Error fetching information"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise OctopusNetClientError(
                "Something really wrong happened!"
            ) from exception

    async def async_fan_speed(self) -> any:
        """Get current fan speed."""
        response = await self._async_request_wrapper(
            method="GET",
            url=f"{self._endpoint}/system/fanspeed",
        )
        LOGGER.debug(response)