"""Sensor platform for APSystems API."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR
from .entity import APSystemsApiEntity
import logging
from homeassistant.const import (
    STATE_UNAVAILABLE,
)
from dataclasses import fields
from .api import APSystemsApiBase
from homeassistant.components.sensor import (
    SensorDeviceClass,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.log(logging.WARN, f"PAT TEST {DOMAIN}")
    _LOGGER.warning("PAT TEST 123 %s", str(entry))

    __options = dict(entry.options)
    _LOGGER.warning("PAT TEST 123 %s", str(__options))
    _LOGGER.warning("PAT TEST 456 %s", str(dir(entry)))
    _devices = [
        APSystemsApiSystemSummarySensor(coordinator, entry, data_key=field.name) 
        for field in fields(APSystemsApiBase.SystemSummaryData)
    ]
    async_add_devices(_devices)


class APSystemsApiSystemSummarySensor(APSystemsApiEntity):
    """apsystems_api Sensor class."""
    data_key: str

    def __init__(self, coordinator, config_entry, data_key: str):
        self.data_key = data_key
        super().__init__(coordinator, config_entry)
        
    # @property
    # def unique_id(self):
    #     return f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_{self.data_key}"

    @property
    def available(self) -> bool:
        _LOGGER.warning("PAT TEST AVAILABLE")
        return True

    @property
    def state(self):

        # _LOGGER.warning(
        #     "PAT TEST XYZ %s",
        #     str(self)
        # )
        _LOGGER.warning(
            "PAT TEST XYZ %s %s", str(self.coordinator), str(self.coordinator.__class__)
        )
        _LOGGER.warning("PAT TEST XYZ %s", str(self.coordinator.data))
        if self.coordinator.data and (value := getattr(self.coordinator.data, self.data_key, None)):
            return value
            return self.coordinator.data.month

        return STATE_UNAVAILABLE  # self.coordinator.data.get("body")

    @property
    def icon(self):
        return ICON

    @property
    def device_class(self):
        return SensorDeviceClass.ENERGY

    # async def async_update(self) -> None:
    #     """Update the entity.

    #     Only used by the generic entity update service.
    #     """
    #     # Ignore manual update requests if the entity is disabled
    #     # if not self.enabled:
    #     #     return

    #     await super().async_update()
    #     # await self.coordinator.async_request_refresh()
