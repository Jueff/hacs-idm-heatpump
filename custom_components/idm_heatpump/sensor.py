"""Sensor platform for idm_heatpump."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_FRIENDLY_NAME
from homeassistant.core import ServiceCall
from homeassistant.helpers import entity_platform

from .sensor_addresses import (
    SENSOR_ADDRESSES,
    SENSOR_NAMES,
    IdmSensorAddress,
)
from .const import DEFAULT_NAME, DOMAIN, SENSOR
from .entity import IdmHeatpumpEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            IdmHeatpumpSensor(
                coordinator,
                entry,
                sensor_name=name,
                icon="mdi:mdi:sun-thermometer-outline",
            )
            for name, s in SENSOR_ADDRESSES.items()
        ]
    )


class IdmHeatpumpSensor(IdmHeatpumpEntity, SensorEntity):
    """IDM heatpump sensor base class"""

    sensor_address: IdmSensorAddress
    _icon: str

    def __init__(self, coordinator, config_entry, sensor_name: str, icon: str):
        super().__init__(coordinator, config_entry)
        self._icon = icon
        if sensor_name not in SENSOR_ADDRESSES:
            raise Exception(f"Sensor not found: {sensor_name}")

        self.sensor_address = SENSOR_ADDRESSES[sensor_name]
        self.entity_description = self.sensor_address.entity_description(config_entry)

    @property
    def sensor_id(self):
        return self.sensor_address.name

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.sensor_address.name)

    @property
    def icon(self):
        return self._icon
