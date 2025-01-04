"""Sample API Client."""
import asyncio
import base64
import hashlib
import hmac
import json
import logging
import typing
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin
from uuid import uuid4
import argparse
import os
import socket

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)


class APSystemsApiResponseException(Exception):
    pass


class APSystemsApiBase:
    @dataclass
    class SystemSummaryData:
        month: float
        year: float
        today: float
        lifetime: float

    base_url: str = "https://api.apsystemsema.com:9282"
    api_app_id: str
    api_app_secret: str
    sid: str
    ecu_id: str
    session: aiohttp.ClientSession

    def __init__(
        self,
        api_app_id: str,
        api_app_secret: str,
        sid: str,
        ecu_id: str,
        session: aiohttp.ClientSession,
    ) -> None:
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.sid = sid
        self.ecu_id = ecu_id
        self.session = session

    def _hmac_sha256(self, key: str, message: str) -> str:
        _hmac = hmac.new(key.encode(), message.encode(), hashlib.sha256)
        return base64.b64encode(_hmac.digest()).decode("utf-8")

    def _request_headers(self, request_method: str, request_path: str) -> str:
        X_CA_AppId = self.api_app_id
        X_CA_Timestamp = f"{int(round(datetime.now().timestamp()))}"
        X_CA_Nonce = uuid4().hex
        X_CA_Signature_Method = "HmacSHA256"
        X_CA_Signature = self._hmac_sha256(
            self.api_app_secret,
            "/".join(
                [
                    X_CA_Timestamp,
                    X_CA_Nonce,
                    X_CA_AppId,
                    request_path.split("/")[-1],
                    request_method.upper(),
                    X_CA_Signature_Method,
                ]
            ),
        )

        return {
            "Content-type": "application/json; charset=UTF-8",
            "x-ca-appid": X_CA_AppId,
            "x-ca-timestamp": X_CA_Timestamp,
            "x-ca-nonce": X_CA_Nonce,
            "x-ca-signature-method": X_CA_Signature_Method,
            "x-ca-signature": X_CA_Signature,
        }

    async def _request(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> aiohttp.ClientResponse:
        try:
            # async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
            async with async_timeout.timeout(TIMEOUT):
                if method.lower() == "get":
                    response = await self.session.get(url, params=data, headers=headers)
                    response.raise_for_status()
                    return response

                elif method.lower() == "put":
                    response = await self.session.put(url, headers=headers, json=data)
                    response.raise_for_status()
                    return response

                elif method.lower() == "patch":
                    response = await self.session.patch(url, headers=headers, json=data)
                    response.raise_for_status()
                    return response

                elif method.lower() == "post":
                    response = await self.session.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    return response

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)

    async def system_summary(self) -> SystemSummaryData:
        request_path = "/user/api/v2/systems/summary/{sid}".format(sid=self.sid)
        _LOGGER.warning("PAT PAT PAT request_path: %s", request_path)
        url = urljoin(self.base_url, request_path)
        headers = self._request_headers("GET", request_path)
        response = await self._request("GET", url, headers=headers)
        data = await response.json()
        if data["code"] != 0:
            raise APSystemsApiBase.ResponseException(
                "Non zero response code: {data}".format(data=json.dumps(data, indent=4))
            )
        return APSystemsApiBase.SystemSummaryData(**data["data"])

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--api_app_id", type=str, default=os.environ.get('APSYSTEMS_API_APP_ID'))
#     parser.add_argument("--api_app_secret", type=str, default=os.environ.get('APSYSTEMS_API_APP_SECRET'))
#     parser.add_argument("--sid", type=str, default=os.environ.get('APSYSTEMS_SID'))
#     parser.add_argument("--ecu_id", type=str, default=os.environ.get('APSYSTEMS_ECU_ID'))
#     args = parser.parse_args()

#     api = APSystemsApiBase(
#         api_app_id=args.api_app_id,
#         api_app_secret=args.api_app_secret,
#         sid=args.sid,
#         ecu_id=args.ecu_id,
#     )

#     print("system_summary", api.system_summary())
#     print("system_summary", api.ecu_minutely_energy())
#     print("system_summary", api.ecu_minutely_energy().latest_power)
#     print("system_summary", api.ecu_minutely_energy().latest_energy)


class APSystemsApiSystemSummaryClient(APSystemsApiBase):
    async def async_get_data(self) -> APSystemsApiBase.SystemSummaryData:
        _LOGGER.warning("PAT PAT PAT async_get_data: %s", "async_get_data")
        return await self.system_summary()
