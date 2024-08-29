"""Test Contracts."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


spacetraders_client = SpaceTradersClient()


def test_list_contracts():
    """Tests."""
    error, result = spacetraders_client.contracts.list_contracts()

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_get_contract():
    """Tests."""
    error, result = spacetraders_client.contracts.get_contract(
        contract_symbol="cm09befg7amhhs60cic3fnpgr",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_accept_contract():
    """Tests."""
    error, result = spacetraders_client.contracts.accept_contract(
        contract_symbol="cm09befg7amhhs60cic3fnpgr",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_deliver_cargo_to_contract():
    """Tests."""
    error, result = spacetraders_client.contracts.deliver_cargo_to_contract(
        contract_symbol="cm09befg7amhhs60cic3fnpgr",
        ship_symbol="",
        trade_symbol="deliver_cargo_to_contract",
        units=60,
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)


def test_fullfill_contract():
    """Tests."""
    error, result = spacetraders_client.contracts.fullfill_contract(
        contract_symbol="cm09befg7amhhs60cic3fnpgr",
    )

    if not result:
        raise Exception(error)

    assert result
    ic(result)
