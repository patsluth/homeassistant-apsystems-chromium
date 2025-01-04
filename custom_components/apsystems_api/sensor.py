"""Sensor platform for APSystems API."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR
from .entity import APSystemsApiEntity
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.log(logging.WARN, f"PAT TEST {DOMAIN}")
    _LOGGER.warning("PAT TEST 123 %s", str(entry))

    __options = dict(entry.options)
    _LOGGER.warning("PAT TEST 123 %s", str(__options))
    _LOGGER.warning("PAT TEST 456 %s", str(dir(entry)))
    async_add_devices([APSystemsApiSystemSummarySensor(coordinator, entry)])


class APSystemsApiSystemSummarySensor(APSystemsApiEntity):
    """apsystems_api Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def available(self) -> bool:
        _LOGGER.warning("PAT TEST AVAILABLE")
        return True

    @property
    def state(self):
        """Return the state of the sensor."""

        # _LOGGER.warning(
        #     "PAT TEST XYZ %s",
        #     str(self)
        # )
        _LOGGER.warning(
            "PAT TEST XYZ %s %s", str(self.coordinator), str(self.coordinator.__class__)
        )
        _LOGGER.warning("PAT TEST XYZ %s", str(self.coordinator.data))
        if self.coordinator.data:
            return self.coordinator.data.month

        return "12345"  # self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "apsystems_api__custom_device_class"

    # async def async_update(self) -> None:
    #     """Update the entity.

    #     Only used by the generic entity update service.
    #     """
    #     # Ignore manual update requests if the entity is disabled
    #     # if not self.enabled:
    #     #     return

    #     await super().async_update()
    #     # await self.coordinator.async_request_refresh()
