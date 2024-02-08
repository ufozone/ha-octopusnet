"""Digital Devices Octopus NET API Client."""
from __future__ import annotations

import asyncio
import socket
import aiohttp
import async_timeout

from homeassistant.helpers.aiohttp_client import HassClientResponse

from .const import (
    LOGGER,
)

class OctopusNetApiError(Exception):
    """Exception to indicate a general client error."""


class OctopusNetApiTimeoutError(OctopusNetApiError):
    """Exception to indicate a timeout error."""


class OctopusNetApiCommunicationError(OctopusNetApiError):
    """Exception to indicate a communication error."""


class OctopusNetApiAuthenticationError(OctopusNetApiError):
    """Exception to indicate an authentication error."""


class OctopusNetApiClient:
    """Octopus NET Client."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int,
        tls: bool,
        verify_ssl: bool,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize."""
        self._host = host
        self._username = username
        self._password = password
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
                LOGGER.debug(response)
                if response.status in (401, 403):
                    raise OctopusNetApiAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return response
        except OctopusNetApiAuthenticationError as exception:
            raise exception
        except TimeoutError as exception:
            raise OctopusNetApiTimeoutError(
                "Timeout error fetching information"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise OctopusNetApiError(
                "Something really wrong happened!"
            ) from exception

    async def async_get_temperature(self) -> float:
        """Get current temperature."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/log/Temperatur.log",
            )
            response_text = await response.text()
            response_lines = response_text.splitlines()
            if len(response_lines) < 3:
                raise OctopusNetApiCommunicationError(
                    "Invalid response",
                )
            return float(response_lines[len(response_lines) - 1])
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_fanspeed(self) -> int:
        """Get current fan speed."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/system/fanspeed",
            )
            response_json = await response.json(
                content_type=None,
            )
            if "speed" not in response_json:
                raise OctopusNetApiCommunicationError(
                    "Invalid response",
                )
            return int(response_json.get("speed", 0))
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_epg(self) -> dict:
        """Get current epg status."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/epg/status",
            )
            response_json = await response.json(
                content_type=None,
            )
            if "status" not in response_json:
                raise OctopusNetApiCommunicationError(
                    "Invalid response",
                )
            return response_json
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_tuner_status(self) -> list:
        """Get current tuner status."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/octoserve/tunerstatus.json",
            )
            response_json = await response.json(
                content_type=None,
            )
            if "TunerList" not in response_json:
                raise OctopusNetApiCommunicationError(
                    "Invalid response",
                )
            return response_json.get("TunerList", [])
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_stream_status(self) -> list:
        """Get current stream status."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/octoserve/streamstatus.json",
            )
            response_json = await response.json(
                content_type=None,
            )
            if "StreamList" not in response_json:
                raise OctopusNetApiCommunicationError(
                    "Invalid response",
                )
            return response_json.get("StreamList", [])
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_channels(self) -> list:
        """Get channel list."""
        try:
            response = await self._async_request_wrapper(
                method="POST",
                url=f"{self._endpoint}/channels/data",
            )
            response_json = await response.json(
                content_type=None,
            )
            if "data" not in response_json:
                raise OctopusNetApiCommunicationError(
                    "Invalid response",
                )
            return response_json.get("data", [])
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetApiCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_start_reboot(self) -> bool:
        """Start reboot."""
        try:
            await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/system/reboot",
            )
            return True
        except Exception as exception:
            raise exception

    async def async_epg_scan(self) -> bool:
        """Start epg scan."""
        try:
            await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/epg/scan",
            )
            return True
        except Exception as exception:
            raise exception
