"""Test Factions."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


spacetraders_client = SpaceTradersClient()


def test_list_factions():
    """Tests."""
    error, result = spacetraders_client.factions.list_factions()

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_faction():
    """Tests."""
    error, result = spacetraders_client.factions.get_faction(
        faction_id="COSMIC",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)
