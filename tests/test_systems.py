"""Test Systems."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


artifacts_client = SpaceTradersClient()


def test_list_systems():
    """Tests."""
    result = artifacts_client.systems.list_systems()

    assert result
    ic(result)


def test_get_system():
    """Tests."""
    result = artifacts_client.systems.get_system(
        system_symbol="X1-GJ54",
    )

    assert result
    ic(result)


def test_list_waypoints_in_system():
    """Tests."""
    result = artifacts_client.systems.list_waypoints_in_system(
        system_symbol="X1-KX49",
        traits="",
        waypoint_type="ENGINEERED_ASTEROID",
    )

    assert result
    ic(result)


def test_get_waypoint():
    """Tests."""
    result = artifacts_client.systems.get_waypoint(
        system_symbol="X1-KX49",
        waypoint_symbol="X1-KX49-A1",
    )

    assert result
    ic(result)


def test_get_marketplace():
    """Tests."""
    result = artifacts_client.systems.get_marketplace(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
    )

    assert result
    ic(result)


def test_get_shipyard():
    """Tests."""
    result = artifacts_client.systems.get_shipyard(
        system_symbol="X1-KX49",
        waypoint_symbol="X1-KX49-C43",
    )

    assert result
    ic(result)


def test_get_jump_gate():
    """Tests."""
    result = artifacts_client.systems.get_jump_gate(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
    )

    assert result
    ic(result)


def test_get_construction_site():
    """Tests."""
    result = artifacts_client.systems.get_construction_site(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
    )

    assert result
    ic(result)


def test_supply_construction_site():
    """Tests."""
    result = artifacts_client.systems.supply_construction_site(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
        ship_symbol="",
        trade_symbol="",
        units="",
    )

    assert result
    ic(result)
