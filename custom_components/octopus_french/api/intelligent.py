"""API client for Octopus Intelligent features."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..octopus_french import OctopusFrenchApiClient

_LOGGER = logging.getLogger(__name__)

MUTATION_TRIGGER_BOOST = """
mutation {
  triggerBoostCharge(input: { accountNumber: "%s" }) {
    krakenflexDevice { krakenflexDeviceId }
  }
}
"""

MUTATION_CANCEL_BOOST = """
mutation {
  cancelBoostCharge(input: { accountNumber: "%s" }) {
    krakenflexDevice { krakenflexDeviceId }
  }
}
"""

QUERY_DEVICE = """
query {
  registeredKrakenflexDevice(accountNumber: "%s") {
    krakenflexDeviceId
    vehicleMake
    vehicleModel
    chargePointMake
    chargePointModel
    status
  }
}
"""


class OctopusIntelligentApiClient:
    """Client for Octopus Intelligent API."""

    def __init__(self, api_client: OctopusFrenchApiClient) -> None:
        """Initialize the client."""
        self.api_client = api_client

    async def trigger_boost_charge(self, account_number: str) -> dict[str, Any] | None:
        """Trigger boost charge."""
        query = MUTATION_TRIGGER_BOOST % account_number
        response = await self.api_client._execute_with_auth(query)
        return response.get("data", {}).get("triggerBoostCharge")

    async def cancel_boost_charge(self, account_number: str) -> dict[str, Any] | None:
        """Cancel boost charge."""
        query = MUTATION_CANCEL_BOOST % account_number
        response = await self.api_client._execute_with_auth(query)
        return response.get("data", {}).get("cancelBoostCharge")

    async def get_device_state(self, account_number: str) -> dict[str, Any] | None:
        """Get device state."""
        query = QUERY_DEVICE % account_number
        response = await self.api_client._execute_with_auth(query)
        return response.get("data", {}).get("registeredKrakenflexDevice")
