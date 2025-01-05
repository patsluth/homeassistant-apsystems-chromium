import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core_config import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .api import APSystemsApiSystemSummaryClient
from .const import CONF_API_APP_ID
from .const import CONF_API_APP_SECRET
from .const import CONF_SID
from .const import CONF_ECU_ID
from .const import DOMAIN
from .const import PLATFORMS
from .const import STARTUP_MESSAGE

SCAN_INTERVAL = timedelta(minutes=60)

_LOGGER: logging.Logger = logging.getLogger(__package__)

class APSystemsApiSystemSummaryDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: APSystemsApiSystemSummaryClient,
    ) -> None:
        """Initialize."""
        self.client = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.client.async_get_data()
        except Exception as exception:
            raise UpdateFailed() from exception