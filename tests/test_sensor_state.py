"""Test the intelligent state sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.octopus_french.coordinator_intelligent import OctopusIntelligentDataUpdateCoordinator
from custom_components.octopus_french.sensor import OctopusIntelligentStateSensor


@pytest.fixture
def mock_coordinator():
    """Mock coordinator."""
    coordinator = MagicMock(spec=OctopusIntelligentDataUpdateCoordinator)
    coordinator.account_number = "A-XXXX"
    coordinator.data = {
        "device": {
            "status": "SMART_CONTROL_CAPABLE",
            "vehicleMake": "Tesla",
            "vehicleModel": "Model 3",
            "chargePointMake": "Tesla",
            "chargePointModel": "V2C Trydan"
        }
    }
    return coordinator


@pytest.fixture
def intelligent_sensor(mock_coordinator):
    """Create intelligent state sensor."""
    return OctopusIntelligentStateSensor(mock_coordinator)


def test_intelligent_sensor_native_value(intelligent_sensor, mock_coordinator):
    """Test native value."""
    assert intelligent_sensor.native_value == "SMART_CONTROL_CAPABLE"


def test_intelligent_sensor_attributes(intelligent_sensor, mock_coordinator):
    """Test extra state attributes."""
    expected = {
        "vehicle_make": "Tesla",
        "vehicle_model": "Model 3",
        "charge_point_make": "Tesla",
        "charge_point_model": "V2C Trydan"
    }
    assert intelligent_sensor.extra_state_attributes == expected
