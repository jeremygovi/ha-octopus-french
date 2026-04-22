"""API client for Octopus Intelligent features."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..octopus_french import OctopusFrenchApiClient

MUTATION_UPDATE_BOOST_CHARGE = """
mutation {
  updateBoostCharge(input: { deviceId: "%s", action: %s }) {
    id
    name
  }
}
"""

QUERY_DEVICES = """
query {
  devices(accountNumber: "%s") {
    id
    name
    status {
      current
      currentState
    }
  }
}
"""

QUERY_VEHICLE_CHARGING_PREFERENCES = """
query {
  vehicleChargingPreferences(accountNumber: "%s") {
    weekdayTargetSoc
    weekdayTargetTime
    weekendTargetSoc
    weekendTargetTime
  }
}
"""

QUERY_FLEX_PLANNED_DISPATCHES = """
query {
  flexPlannedDispatches(deviceId: "%s") {
    start
    end
  }
}
"""


class OctopusIntelligentApiClient:
    """Client for Octopus Intelligent API."""

    def __init__(self, api_client: OctopusFrenchApiClient) -> None:
        """Initialize the client."""
        self.api_client = api_client

    async def _update_boost_charge(self, device_id: str, action: str) -> tuple[dict[str, Any] | None, list[str]]:
        """Update boost charge (trigger or cancel). Returns (data, refusal_reasons)."""
        query = MUTATION_UPDATE_BOOST_CHARGE % (device_id, action)
        response = await self.api_client._execute_with_auth(query)

        refusal_reasons: list[str] = []
        if response and "errors" in response:
            for error in response.get("errors", []):
                extensions = error.get("extensions", {})
                refusal_reasons.extend(extensions.get("boostChargeRefusalReasons", []))

        data = response.get("data", {}).get("updateBoostCharge") if response else None
        return data, refusal_reasons

    async def trigger_boost_charge(self, device_id: str) -> tuple[dict[str, Any] | None, list[str]]:
        """Trigger boost charge. Returns (data, refusal_reasons)."""
        return await self._update_boost_charge(device_id, "BOOST")

    async def cancel_boost_charge(self, device_id: str) -> tuple[dict[str, Any] | None, list[str]]:
        """Cancel boost charge. Returns (data, refusal_reasons)."""
        return await self._update_boost_charge(device_id, "CANCEL")

    async def get_devices(self, account_number: str) -> list[dict[str, Any]]:
        """Get list of Intelligent devices for an account."""
        query = QUERY_DEVICES % account_number
        response = await self.api_client._execute_with_auth(query)
        return response.get("data", {}).get("devices", []) if response else []

    async def get_vehicle_charging_preferences(self, account_number: str) -> dict[str, Any]:
        """Get vehicle charging preferences for an account."""
        query = QUERY_VEHICLE_CHARGING_PREFERENCES % account_number
        response = await self.api_client._execute_with_auth(query)
        return response.get("data", {}).get("vehicleChargingPreferences", {}) if response else {}

    async def get_flex_planned_dispatches(self, device_id: str) -> list[dict[str, Any]]:
        """Get planned flex dispatch windows for a device."""
        query = QUERY_FLEX_PLANNED_DISPATCHES % device_id
        response = await self.api_client._execute_with_auth(query)
        return response.get("data", {}).get("flexPlannedDispatches", []) if response else []


