"""Test Fleet."""

from time import sleep

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


artifacts_client = SpaceTradersClient()


def test_list_ships():
    """Tests."""
    error, result = artifacts_client.fleet.list_ships()

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_get_ship():
    """Tests."""
    error, result = artifacts_client.fleet.get_ship(
        ship_symbol="BILLY1-1",
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_get_ship_cargo():
    """Tests."""
    error, result = artifacts_client.fleet.get_ship_cargo(
        ship_symbol="BILLY1-1",
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)


def test_orbit_ship():
    """Tests."""
    error, result = artifacts_client.fleet.orbit_ship(
        ship_symbol="BILLY1-1",
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_navigate_ship():
    """Tests."""
    error, result = artifacts_client.fleet.navigate_ship(
        ship_symbol="BILLY1-1",
        waypoint_symbol="X1-KX49-XC5C",
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_dock_ship():
    """Tests."""
    error, result = artifacts_client.fleet.dock_ship(
        ship_symbol="BILLY1-1",
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_refuel_ship():
    """Tests."""
    error, result = artifacts_client.fleet.refuel_ship(
        ship_symbol="BILLY1-1",
        units=43,
        from_cargo=False,
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_extract_resources():
    """Tests."""
    error, result = artifacts_client.fleet.extract_resources(
        ship_symbol="BILLY1-1",
    )

    if not result:
        print(error)

    else:
        assert result
        ic(result)
        sleep(result.data.cooldown.remainingSeconds)


def test_cargo_resources():
    """Tests."""
    error, ships = artifacts_client.fleet.list_ships()

    if not ships:
        print(error)

    else:
        for ship in ships.data:
            print(f"* {ship.symbol}")
            error, cargo = artifacts_client.fleet.get_ship_cargo(ship_symbol=ship.symbol)

            if not cargo:
                print(error)

            else:
                for resource in cargo.data.inventory:
                    print(f"- {resource.units} {resource.name}")

                print("\n")
