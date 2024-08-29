"""Test Contracts."""

from icecream import ic

from spacetraders_python_sdk import SpaceTradersClient


artifacts_client = SpaceTradersClient()


def test_list_contracts():
    """Tests."""
    result = artifacts_client.contracts.list_contracts()

    assert result
    ic(result)


def test_get_contract():
    """Tests."""
    result = artifacts_client.contracts.get_contract(
        contract_id="cm09befg7amhhs60cic3fnpgr",
    )

    assert result
    ic(result)


def test_accept_contract():
    """Tests."""
    result = artifacts_client.contracts.accept_contract(
        contract_id="cm09befg7amhhs60cic3fnpgr",
    )

    assert result
    ic(result)


def test_deliver_cargo_to_contract():
    """Tests."""
    result = artifacts_client.contracts.deliver_cargo_to_contract(
        contract_id="cm09befg7amhhs60cic3fnpgr",
        ship_symbol="",
        trade_symbol="deliver_cargo_to_contract",
        units=60,
    )

    assert result
    ic(result)


def test_fullfill_contract():
    """Tests."""
    result = artifacts_client.contracts.fullfill_contract(
        contract_id="cm09befg7amhhs60cic3fnpgr",
    )

    assert result
    ic(result)
