"""Test the intelligent API client."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from aioresponses import aioresponses

from custom_components.octopus_french.api.intelligent import OctopusIntelligentApiClient
from custom_components.octopus_french.octopus_french import GRAPHQL_ENDPOINT


@pytest.fixture
def mock_api_client():
    """Mock the main API client."""
    client = MagicMock()
    client._execute_with_auth = AsyncMock()
    return client


@pytest.fixture
def intelligent_client(mock_api_client):
    """Create intelligent client."""
    return OctopusIntelligentApiClient(mock_api_client)


@pytest.mark.asyncio
async def test_trigger_boost_charge_success(intelligent_client, mock_api_client):
    """Test successful boost charge trigger."""
    mock_api_client._execute_with_auth.return_value = {
        "data": {
            "triggerBoostCharge": {
                "krakenflexDevice": {"krakenflexDeviceId": "abc-123"}
            }
        }
    }

    result = await intelligent_client.trigger_boost_charge("A-XXXX")

    assert result == {"krakenflexDevice": {"krakenflexDeviceId": "abc-123"}}
    mock_api_client._execute_with_auth.assert_called_once()


@pytest.mark.asyncio
async def test_trigger_boost_charge_refused(intelligent_client, mock_api_client):
    """Test boost charge refused."""
    mock_api_client._execute_with_auth.return_value = {
        "errors": [{
            "message": "Unable to trigger boost charge.",
            "extensions": {
                "errorCode": "KT-CT-4357",
                "boostChargeRefusalReasons": ["BC_DEVICE_DISCONNECTED"]
            }
        }],
        "data": {"triggerBoostCharge": None}
    }

    result = await intelligent_client.trigger_boost_charge("A-XXXX")

    assert result is None
    mock_api_client._execute_with_auth.assert_called_once()


@pytest.mark.asyncio
async def test_cancel_boost_charge(intelligent_client, mock_api_client):
    """Test cancel boost charge."""
    mock_api_client._execute_with_auth.return_value = {
        "data": {
            "cancelBoostCharge": {
                "krakenflexDevice": {"krakenflexDeviceId": "abc-123"}
            }
        }
    }

    result = await intelligent_client.cancel_boost_charge("A-XXXX")

    assert result == {"krakenflexDevice": {"krakenflexDeviceId": "abc-123"}}
    mock_api_client._execute_with_auth.assert_called_once()


@pytest.mark.asyncio
async def test_get_device_state(intelligent_client, mock_api_client):
    """Test get device state."""
    mock_api_client._execute_with_auth.return_value = {
        "data": {
            "registeredKrakenflexDevice": {
                "krakenflexDeviceId": "abc-123",
                "status": "SMART_CONTROL_CAPABLE"
            }
        }
    }

    result = await intelligent_client.get_device_state("A-XXXX")

    assert result == {
        "krakenflexDeviceId": "abc-123",
        "status": "SMART_CONTROL_CAPABLE"
    }
    mock_api_client._execute_with_auth.assert_called_once()
