"""Test Systems."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


spacetraders_client = SpaceTradersClient()


def test_list_systems():
    """Tests."""
    error, result = spacetraders_client.systems.list_systems()

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_system():
    """Tests."""
    error, result = spacetraders_client.systems.get_system(
        system_symbol="X1-GJ54",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_list_waypoints_in_system():
    """Tests."""
    error, result = spacetraders_client.systems.list_waypoints_in_system(
        system_symbol="X1-KX49",
        traits="",
        waypoint_type="ENGINEERED_ASTEROID",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_waypoint():
    """Tests."""
    error, result = spacetraders_client.systems.get_waypoint(
        system_symbol="X1-KX49",
        waypoint_symbol="X1-KX49-XC5C",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_market():
    """Tests."""
    error, result = spacetraders_client.systems.get_market(
        system_symbol="X1-KX49",
        waypoint_symbol="X1-KX49-G51",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_list_system_markets():
    """Tests"""
    error, market_waypoints = spacetraders_client.systems.list_waypoints_in_system(
        system_symbol="X1-KX49",
        traits="MARKETPLACE",
        waypoint_type="",
    )

    if not market_waypoints:
        raise Exception(error)

    for waypoint in market_waypoints.data:
        error, marketplace = spacetraders_client.systems.get_market(
            system_symbol="X1-KX49",
            waypoint_symbol=waypoint.symbol,
        )

        if not marketplace:
            raise Exception(error)

        assert marketplace
        ic(marketplace)


def test_get_shipyard():
    """Tests."""
    error, result = spacetraders_client.systems.get_shipyard(
        system_symbol="X1-KX49",
        waypoint_symbol="X1-KX49-C43",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_jump_gate():
    """Tests."""
    error, result = spacetraders_client.systems.get_jump_gate(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_construction_site():
    """Tests."""
    error, result = spacetraders_client.systems.get_construction_site(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_supply_construction_site():
    """Tests."""
    error, result = spacetraders_client.systems.supply_construction_site(
        system_symbol="X1-GJ54",
        waypoint_symbol="X1-GJ54-ZD2F",
        ship_symbol="",
        trade_symbol="",
        units="",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)
