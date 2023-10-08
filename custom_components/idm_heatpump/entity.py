"""IdmHeatpumpEntity class."""
from abc import abstractmethod

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .coordinator import IdmHeatpumpDataUpdateCoordinator
from .const import CONF_DISPLAY_NAME, CONF_HOSTNAME, DOMAIN, MANUFACTURER, MODEL_MAIN, MODEL_ZONE
from .sensor_addresses import BaseSensorAddress


class IdmHeatpumpEntity(CoordinatorEntity):
    """IdmHeatpumpEntity."""

    sensor_address: BaseSensorAddress
    coordinator: IdmHeatpumpDataUpdateCoordinator

    def __init__(self, coordinator: IdmHeatpumpDataUpdateCoordinator, config_entry: ConfigEntry):
        """Create entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    @abstractmethod
    def sensor_id(self) -> str:
        """Return the unique ID for this sensor."""

    @property
    def available(self) -> bool:
        """Return wether this sensor is available."""
        return self.sensor_address in self.coordinator.heatpump.sensors

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{slugify(self.config_entry.data.get(CONF_HOSTNAME))}_{self.sensor_id}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        zone = self.sensor_address.zone_id
        if zone is not None:
            return DeviceInfo(
                identifiers={
                    (DOMAIN, f"{self.config_entry.entry_id}_zone_{zone+1}")
                },
                name=f"{self.config_entry.data.get(CONF_DISPLAY_NAME)} Zone {zone+1}",
                model=MODEL_ZONE,
                manufacturer=MANUFACTURER,
                via_device=(DOMAIN, self.config_entry.entry_id),
            )

        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=self.config_entry.data.get(CONF_DISPLAY_NAME),
            model=MODEL_MAIN,
            manufacturer=MANUFACTURER,
        )

    @ property
    def extra_state_attributes(self):
        """Return extra attributes."""
        return {
            "integration": DOMAIN,
        }
