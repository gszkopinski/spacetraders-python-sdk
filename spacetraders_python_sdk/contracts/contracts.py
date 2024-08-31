"""Contacts."""

from typing import Annotated, Tuple

import requests

from pydantic import Field

from ..models.models import (
    AcceptContractResponseSchema,
    ContractResponseSchema,
    ListContractsResponseSchema,
)


class Contracts:
    """Contracts."""

    def __init__(
        self,
        api_url: str,
        session: requests.Session,
    ) -> None:
        """Init."""
        self.api_url = api_url
        self.session = session

    def list_contracts(
        self,
        page: Annotated[int, Field(description="What entry offset to request.", ge=1, default=1)] = 1,
        limit: Annotated[int, Field(description="How many entries to return per page.", ge=1, le=20, default=10)] = 10,
    ) -> Tuple[str, ListContractsResponseSchema | None]:
        """Return a paginated list of all your contracts."""
        try:
            parameters = f"page={page}"
            parameters += f"&limit={limit}"

            response = self.session.get(
                url=f"{self.api_url}/my/contracts?{parameters}",
            )

            response.raise_for_status()

            return (
                "Succesfully listed contracts.",
                ListContractsResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "contracts not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_contract(
        self,
        contract_id: Annotated[str, Field(description="The contract ID.")]
    ) -> Tuple[str, ContractResponseSchema | None]:
        """Get the details of a contract by ID."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/my/contracts/{contract_id}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched contract details.",
                ContractResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "contract not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None

    def accept_contract(
        self,
        contract_id: Annotated[str, Field(description="The contract ID.")]
    ) -> Tuple[str, AcceptContractResponseSchema | None]:
        """Accept a contract by ID.

        You can only accept contracts that were offered to you, were not accepted yet,
        and whose deadlines has not passed yet.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/contracts/{contract_id}/accept",
            )

            response.raise_for_status()

            return (
                "Succesfully accepted contract.",
                AcceptContractResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "contract not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None

    def deliver_cargo_to_contract(
        self,
        contract_id: Annotated[str, Field(description="The ID of the contract.")],
        ship_symbol: Annotated[str, Field(description=(
            "Symbol of a ship located in the destination to deliver a contract"
            "and that has a good to deliver in its cargo."
        ))],
        trade_symbol: Annotated[str, Field(description="The symbol of the good to deliver.")],
        units: Annotated[int, Field(description="Amount of units to deliver.")],

    ) -> Tuple[str, AcceptContractResponseSchema | None]:
        """Deliver cargo to a contract.

        In order to use this API, a ship must be at the delivery location
        (denoted in the delivery terms as destinationSymbol of a contract)
        and must have a number of units of a good required by this contract in its cargo.

        Cargo that was delivered will be removed from the ship's cargo.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/contracts/{contract_id}/deliver",
                json={
                    "shipSymbol": ship_symbol,
                    "tradeSymbol": trade_symbol,
                    "units": units,
                },
            )

            response.raise_for_status()

            return (
                "Succesfully accepted contract.",
                AcceptContractResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "contract not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None

    def fullfill_contract(
        self,
        contract_id: Annotated[str, Field(description="The ID of the contract to fulfill.")],
    ) -> Tuple[str, AcceptContractResponseSchema | None]:
        """Fulfill a contract.

        Can only be used on contracts that have all of their delivery terms fulfilled.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/contracts/{contract_id}/fullfill",
            )

            response.raise_for_status()

            return (
                "Succesfully accepted contract.",
                AcceptContractResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "contract not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None
