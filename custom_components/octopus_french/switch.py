"""Switches for Octopus Intelligent features."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity
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
    """Set up the switches."""
    coordinator: OctopusIntelligentDataUpdateCoordinator = hass.data["octopus_french"][config_entry.entry_id]["intelligent_coordinator"]
    async_add_entities([
        OctopusIntelligentBumpChargeSwitch(coordinator),
        OctopusIntelligentSmartChargeSwitch(coordinator),
    ])


class OctopusIntelligentBumpChargeSwitch(CoordinatorEntity, SwitchEntity):
    """Switch for bump charge."""

    def __init__(self, coordinator: OctopusIntelligentDataUpdateCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.account_number}_bump_charge"
        self._attr_name = "Octopus Intelligent Bump Charge"
        self._attr_device_class = "switch"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        status = self.coordinator.data.get("device", {}).get("status")
        return status == "BOOSTING"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "refusal_reasons": self.coordinator.data.get("boost_refusal_reasons", []),
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        result = await self.coordinator.intelligent_client.trigger_boost_charge(self.coordinator.account_number)
        if result is None:
            # Check for errors
            # In real implementation, parse response for errors
            self.coordinator.data["boost_refusal_reasons"] = ["BC_DEVICE_DISCONNECTED"]  # Example
        else:
            self.coordinator.data["boost_refusal_reasons"] = []
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.intelligent_client.cancel_boost_charge(self.coordinator.account_number)
        self.coordinator.data["boost_refusal_reasons"] = []
        await self.coordinator.async_request_refresh()


class OctopusIntelligentSmartChargeSwitch(CoordinatorEntity, SwitchEntity):
    """Switch for smart charge."""

    def __init__(self, coordinator: OctopusIntelligentDataUpdateCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.account_number}_smart_charge"
        self._attr_name = "Octopus Intelligent Smart Charge"
        self._attr_device_class = "switch"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        status = self.coordinator.data.get("device", {}).get("status")
        return status in ["SMART_CONTROL_CAPABLE", "CONNECTED"]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # Implement smart charge activation if available
        pass

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # Implement smart charge deactivation if available
        pass
