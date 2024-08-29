"""Test Agents."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


spacetraders_client = SpaceTradersClient()


def test_get_agent():
    """Tests."""
    error, result = spacetraders_client.agents.get_agent()

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_list_agents():
    """Tests."""
    error, result = spacetraders_client.agents.list_agents()

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_public_agent():
    """Tests."""
    error, result = spacetraders_client.agents.get_public_agent()

    if not result:
        raise Exception(error)

    assert result
    ic(result)
