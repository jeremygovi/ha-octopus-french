"""Test the bump charge switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.octopus_french.coordinator_intelligent import OctopusIntelligentDataUpdateCoordinator
from custom_components.octopus_french.switch import OctopusIntelligentBumpChargeSwitch


@pytest.fixture
def mock_coordinator():
    """Mock coordinator."""
    coordinator = MagicMock(spec=OctopusIntelligentDataUpdateCoordinator)
    coordinator.account_number = "A-XXXX"
    coordinator.data = {"device": {"status": "CONNECTED"}, "boost_refusal_reasons": []}
    coordinator.intelligent_client = MagicMock()
    coordinator.intelligent_client.trigger_boost_charge = AsyncMock()
    coordinator.intelligent_client.cancel_boost_charge = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def bump_charge_switch(mock_coordinator):
    """Create bump charge switch."""
    return OctopusIntelligentBumpChargeSwitch(mock_coordinator)


@pytest.mark.asyncio
async def test_bump_charge_switch_on(bump_charge_switch, mock_coordinator):
    """Test turning on bump charge."""
    mock_coordinator.intelligent_client.trigger_boost_charge.return_value = {"krakenflexDevice": {"krakenflexDeviceId": "abc"}}

    await bump_charge_switch.async_turn_on()

    mock_coordinator.intelligent_client.trigger_boost_charge.assert_called_once_with("A-XXXX")
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_bump_charge_switch_off(bump_charge_switch, mock_coordinator):
    """Test turning off bump charge."""
    await bump_charge_switch.async_turn_off()

    mock_coordinator.intelligent_client.cancel_boost_charge.assert_called_once_with("A-XXXX")
    mock_coordinator.async_request_refresh.assert_called_once()


def test_bump_charge_switch_is_on_boosting(bump_charge_switch, mock_coordinator):
    """Test is_on when boosting."""
    mock_coordinator.data["device"]["status"] = "BOOSTING"
    assert bump_charge_switch.is_on is True


def test_bump_charge_switch_is_on_not_boosting(bump_charge_switch, mock_coordinator):
    """Test is_on when not boosting."""
    mock_coordinator.data["device"]["status"] = "CONNECTED"
    assert bump_charge_switch.is_on is False


def test_bump_charge_switch_attributes(bump_charge_switch, mock_coordinator):
    """Test extra state attributes."""
    mock_coordinator.data["boost_refusal_reasons"] = ["BC_DEVICE_DISCONNECTED"]
    assert bump_charge_switch.extra_state_attributes == {"refusal_reasons": ["BC_DEVICE_DISCONNECTED"]}
