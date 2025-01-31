"""Sensor platform for APSystems API."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR

from .const import ATTRIBUTION
from .const import NAME
from .const import VERSION

from .entity import APSystemsApiEntity
import logging
from homeassistant.const import (
    STATE_UNAVAILABLE,
)
from dataclasses import fields
from .api import APSystemsApiBase, APSystemsApiSystemSummaryClient
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity
)
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import DiscoveryInfoType

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        APSystemsApiSystemSummarySensor(coordinator, config_entry, data_key=field.name) 
        for field in fields(APSystemsApiBase.SystemSummaryData)
    )
    
    async_add_entities(
        APSystemsApiECUMinutelyEnergyDataSensor(coordinator, config_entry, data_key=field.name) 
        for field in ["latest_power", "latest_energy"]
    )


class APSystemsApiSystemSummarySensor(APSystemsApiEntity, SensorEntity):
    """apsystems_api Sensor class."""
    data_key: str

    def __init__(self, coordinator, config_entry, data_key: str):
        self.data_key = data_key
        self.entity_id = generate_entity_id(
            entity_id_format="sensor.{}", 
            name=self.name,
            hass=coordinator.hass
        )
        # self._attr_unique_id = f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"
        self._attr_unique_id = f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"
        super().__init__(coordinator, config_entry)
        
    # @property
    # def unique_id(self):
    #     return f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"



    # @property
    # def entity_id(self):
    #     _LOGGER.warning("PAT TEST entity_id %s", str(super(APSystemsApiSystemSummarySensor, self).entity_id))
    #     return f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_{self.data_key}"
    
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def available(self) -> bool:
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
        data: APSystemsApiSystemSummaryClient.SystemData = self.coordinator.data
        _LOGGER.warning("PAT TEST XYZ %s", str(data))
        if data and data.ecu_minutely_energy and (value := getattr(data.ecu_minutely_energy, self.data_key, None)):
            return value
            return self.coordinator.data.month

        return STATE_UNAVAILABLE  # self.coordinator.data.get("body")

    @property
    def icon(self):
        return ICON

    @property
    def device_class(self):
        if self.data_key == "latest_power":
            return SensorDeviceClass.POWER
        if self.data_key == "latest_energy":
            return SensorDeviceClass.POWER
        return None

    # async def async_update(self) -> None:
    #     """Update the entity.

    #     Only used by the generic entity update service.
    #     """
    #     # Ignore manual update requests if the entity is disabled
    #     # if not self.enabled:
    #     #     return

    #     await super().async_update()
    #     # await self.coordinator.async_request_refresh()


class APSystemsApiECUMinutelyEnergyDataSensor(APSystemsApiEntity, SensorEntity):
    """apsystems_api Sensor class."""
    data_key: str

    def __init__(self, coordinator, config_entry, data_key: str):
        self.data_key = data_key
        self.entity_id = generate_entity_id(
            entity_id_format="sensor.{}", 
            name=self.name,
            hass=coordinator.hass
        )
        # self._attr_unique_id = f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"
        self._attr_unique_id = f"{super(APSystemsApiECUMinutelyEnergyDataSensor, self).unique_id}_{self.name}"
        super().__init__(coordinator, config_entry)
        
    # @property
    # def unique_id(self):
    #     return f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"



    # @property
    # def entity_id(self):
    #     _LOGGER.warning("PAT TEST entity_id %s", str(super(APSystemsApiSystemSummarySensor, self).entity_id))
    #     return f"{super(APSystemsApiSystemSummarySensor, self).unique_id}_{self.name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_{self.data_key}"
    
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def available(self) -> bool:
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
        data: APSystemsApiSystemSummaryClient.SystemData = self.coordinator.data
        _LOGGER.warning("PAT TEST XYZ %s", str(data))
        if data and data.system_summary and (value := getattr(data.system_summary, self.data_key, None)):
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
