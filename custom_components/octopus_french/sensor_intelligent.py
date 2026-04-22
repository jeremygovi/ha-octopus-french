"""Sensor for Octopus Intelligent state."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator_intelligent import OctopusIntelligentDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor."""
    coordinator: OctopusIntelligentDataUpdateCoordinator = hass.data["octopus_french"][config_entry.entry_id]["intelligent_coordinator"]
    async_add_entities([OctopusIntelligentStateSensor(coordinator)])


class OctopusIntelligentStateSensor(CoordinatorEntity, SensorEntity):
    """Sensor for intelligent device state."""

    def __init__(self, coordinator: OctopusIntelligentDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.account_number}_intelligent_state"
        self._attr_name = "Octopus Intelligent State"
        self._attr_device_class = "sensor"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("device", {}).get("status")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return extra state attributes."""
        device = self.coordinator.data.get("device", {})
        return {
            "vehicle_make": device.get("vehicleMake"),
            "vehicle_model": device.get("vehicleModel"),
            "charge_point_make": device.get("chargePointMake"),
            "charge_point_model": device.get("chargePointModel"),
        }
