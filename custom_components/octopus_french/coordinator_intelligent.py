"""Data update coordinator for Octopus Intelligent features."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api.intelligent import OctopusIntelligentApiClient

if TYPE_CHECKING:
    from .octopus_french import OctopusFrenchApiClient

_LOGGER = logging.getLogger(__name__)


class OctopusIntelligentDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Intelligent API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: OctopusFrenchApiClient,
        account_number: str,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Octopus Intelligent",
            update_interval=timedelta(minutes=5),  # More frequent for intelligent
        )
        self.api_client = api_client
        self.intelligent_client = OctopusIntelligentApiClient(api_client)
        self.account_number = account_number

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            device_data = await self.intelligent_client.get_device_state(self.account_number)
            if device_data:
                return {
                    "device": device_data,
                    "boost_refusal_reasons": [],  # Will be set by switches
                }
            return {}
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Intelligent API: {err}") from err
