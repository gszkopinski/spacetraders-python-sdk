"""Test Agents."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


artifacts_client = SpaceTradersClient()


def test_get_agent():
    """Tests."""
    result = artifacts_client.agents.get_agent()

    assert result
    ic(result)


def test_list_agents():
    """Tests."""
    result = artifacts_client.agents.list_agents()

    assert result
    ic(result)


def test_get_public_agent():
    """Tests."""
    result = artifacts_client.agents.get_public_agent()

    assert result
    ic(result)
