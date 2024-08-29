"""Test Status."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


spacetraders_client = SpaceTradersClient()


def test_get_status():
    """Tests."""
    result = spacetraders_client.get_status()

    assert result
    ic(result)
