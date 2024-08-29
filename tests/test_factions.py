"""Test Factions."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


artifacts_client = SpaceTradersClient()


def test_list_factions():
    """Tests."""
    result = artifacts_client.factions.list_factions()

    assert result
    ic(result)


def test_get_faction():
    """Tests."""
    result = artifacts_client.factions.get_faction(
        faction_id="COSMIC",
    )

    assert result
    ic(result)
