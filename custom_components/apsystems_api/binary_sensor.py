"""Binary sensor platform for APSystems API."""
from homeassistant.components.binary_sensor import BinarySensorEntity
_LOGGER: logging.Logger = logging.getLogger(__package__)

from .const import BINARY_SENSOR
from .const import BINARY_SENSOR_DEVICE_CLASS
from .const import DEFAULT_NAME
from .const import DOMAIN
from .entity import APSystemsApiEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([APSystemsApiBinarySensor(coordinator, entry)])


class APSystemsApiBinarySensor(APSystemsApiEntity, BinarySensorEntity):
    """apsystems_api binary_sensor class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _LOGGER.error(
            "PAT TEST %s",
            str(self.config_entry)
        )

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{BINARY_SENSOR}"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BINARY_SENSOR_DEVICE_CLASS

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get("title", "") == "foo"
