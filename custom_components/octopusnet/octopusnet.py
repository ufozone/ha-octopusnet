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


class OctopusNetClientCommunicationError(OctopusNetClientError):
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
                if response.status in (404, 500, 501, 502, 503, 504):
                    raise OctopusNetClientError(
                        "Not supported",
                    )
                response.raise_for_status()
                return response
        except asyncio.TimeoutError as exception:
            raise OctopusNetClientTimeoutError(
                "Timeout error fetching information"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise OctopusNetClientCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise OctopusNetClientError(
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
                raise OctopusNetClientCommunicationError()
            return float(response_lines[len(response_lines) - 1])
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetClientCommunicationError(
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
                raise OctopusNetClientCommunicationError()
            return int(response_json.get("speed", 0))
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetClientCommunicationError(
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
                raise OctopusNetClientCommunicationError()
            return response_json
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetClientCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_tuner_status(self) -> dict:
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
                raise OctopusNetClientCommunicationError()
            return response_json.get("TunerList", {})
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetClientCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_get_stream_status(self) -> dict:
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
                raise OctopusNetClientCommunicationError()
            return response_json.get("StreamList", {})
        except aiohttp.ContentTypeError as exception:
            raise OctopusNetClientCommunicationError(
                "Error fetching information"
            ) from exception
        except Exception as exception:
            raise exception

    async def async_start_reboot(self) -> bool:
        """Start reboot."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/system/reboot",
            )
            return True
        except Exception as exception:
            raise exception

    async def async_epg_scan(self) -> bool:
        """Start epg scan."""
        try:
            response = await self._async_request_wrapper(
                method="GET",
                url=f"{self._endpoint}/epg/scan",
            )
            return True
        except Exception as exception:
            raise exception
