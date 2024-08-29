"""Test Fleet."""

from time import sleep

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


spacetraders_client = SpaceTradersClient()


def test_list_ships():
    """Tests."""
    error, result = spacetraders_client.fleet.list_ships()

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_ship():
    """Tests."""
    error, result = spacetraders_client.fleet.get_ship(
        ship_symbol="BILLY1-1",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_ship_cargo():
    """Tests."""
    error, result = spacetraders_client.fleet.get_ship_cargo(
        ship_symbol="BILLY1-1",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_orbit_ship():
    """Tests."""
    error, action = spacetraders_client.fleet.orbit_ship(
        ship_symbol="BILLY1-1",
    )

    if not action:
        raise Exception(error)

    assert action
    ic(action)
    sleep(action.data.cooldown.remainingSeconds)


def test_navigate_ship():
    """Tests."""
    error, action = spacetraders_client.fleet.navigate_ship(
        ship_symbol="BILLY1-1",
        waypoint_symbol="X1-KX49-XC5C",
    )

    if not action:
        raise Exception(error)

    assert action
    ic(action)
    sleep(action.data.cooldown.remainingSeconds)


def test_dock_ship():
    """Tests."""
    error, action = spacetraders_client.fleet.dock_ship(
        ship_symbol="BILLY1-1",
    )

    if not action:
        raise Exception(error)

    assert action
    ic(action)
    sleep(action.data.cooldown.remainingSeconds)


def test_refuel_ship():
    """Tests."""
    error, action = spacetraders_client.fleet.refuel_ship(
        ship_symbol="BILLY1-1",
        units=43,
        from_cargo=False,
    )

    if not action:
        raise Exception(error)

    assert action
    ic(action)
    sleep(action.data.cooldown.remainingSeconds)


def test_extract_resources():
    """Tests."""
    error, action = spacetraders_client.fleet.extract_resources(
        ship_symbol="BILLY1-1",
    )

    if not action:
        raise Exception(error)

    assert action
    ic(action)
    sleep(action.data.cooldown.remainingSeconds)


def test_cargo_resources():
    """Tests."""
    error, ships = spacetraders_client.fleet.list_ships()

    if not ships:
        raise Exception(error)

    for ship in ships.data:
        print(f"* {ship.symbol}")
        error, cargo = spacetraders_client.fleet.get_ship_cargo(ship_symbol=ship.symbol)

        if not cargo:
            raise Exception(error)

        for resource in cargo.data.inventory:
            print(f"- {resource.units} {resource.name}")

        print("\n")
