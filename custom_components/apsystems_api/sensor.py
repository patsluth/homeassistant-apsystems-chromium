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
    _LOGGER.warning(
        "PAT TEST 123 %s",
        str(entry)
    )

    __options = dict(entry.options)
    _LOGGER.warning(
        "PAT TEST 123 %s",
        str(__options)
    )
    _LOGGER.warning(
        "PAT TEST 456 %s",
        str(dir(entry))
    )
    async_add_devices([APSystemsApiSensor(coordinator, entry)])


class APSystemsApiSensor(APSystemsApiEntity):
    """apsystems_api Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "apsystems_api__custom_device_class"
