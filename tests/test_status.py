"""Test Status."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


artifacts_client = SpaceTradersClient()


def test_get_status():
    """Tests."""
    result = artifacts_client.get_status()

    assert result
    ic(result)
