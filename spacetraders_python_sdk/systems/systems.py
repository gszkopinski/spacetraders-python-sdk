"""Systems."""

from typing import Annotated, Tuple

import requests

from pydantic import Field

from ..models.models import (
    ConstructionResponseSchema,
    JumpGateResponseSchema,
    ListSystemsResponseSchema,
    ListWaypointsResponseSchema,
    MarketResponseSchema,
    ShipyardResponseSchema,
    SupplyConstructionResponseSchema,
    SystemResponseSchema,
    WaypointResponseSchema,
    WaypointTypeEnum,
)


class Systems:
    """Systems."""

    def __init__(
        self,
        api_url: str,
        session: requests.Session,
    ) -> None:
        """Init."""
        self.api_url = api_url
        self.session = session

    def list_systems(
        self,
        page: Annotated[int, Field(description="What entry offset to request.", ge=1, default=1)] = 1,
        limit: Annotated[int, Field(description="How many entries to return per page.", ge=1, le=20, default=10)] = 10,
    ) -> Tuple[str, ListSystemsResponseSchema | None]:
        """Return a paginated list of all the systems in the game."""
        try:
            parameters = f"page={page}"
            parameters += f"&limit={limit}"

            response = self.session.get(
                url=f"{self.api_url}/systems?{parameters}",
            )

            response.raise_for_status()

            return (
                "Succesfully fetched systems.",
                ListSystemsResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_system(
        self,
        system_symbol: Annotated[str, Field(description="The system ID.")],
    ) -> Tuple[str, SystemResponseSchema | None]:
        """Get the details of a system by ID."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched system details.",
                SystemResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def list_waypoints_in_system(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol")],
        traits: Annotated[str, Field(description="The unique identifier of the trait.")],
        waypoint_type: Annotated[WaypointTypeEnum, Field(description="Filter waypoints by type.", alias="type")],
        page: Annotated[int, Field(description="What entry offset to request.", ge=1, default=1)] = 1,
        limit: Annotated[int, Field(description="How many entries to return per page.", ge=1, le=20, default=10)] = 10,
    ) -> Tuple[str, ListWaypointsResponseSchema | None]:
        """Return a paginated list of all the systems in the game."""
        try:
            parameters = f"page={page}"
            parameters += f"&limit={limit}"
            parameters += f"&traits={traits}" if traits else ""
            parameters += f"&type={waypoint_type}" if waypoint_type else ""

            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints?{parameters}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched all waypoints in the system.",
                ListWaypointsResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_waypoint(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol.")],
        waypoint_symbol: Annotated[str, Field(description="The waypoint symbol.")],
    ) -> Tuple[str, WaypointResponseSchema | None]:
        """View the details of a waypoint.

        If the waypoint is uncharted, it will return the 'Uncharted' trait instead of its actual traits.
        """
        try:
            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched waypoint.",
                WaypointResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_market(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol.")],
        waypoint_symbol: Annotated[str, Field(description="The waypoint symbol.")],
    ) -> Tuple[str, MarketResponseSchema | None]:
        """Retrieve imports, exports and exchange data from a marketplace.

        Requires a waypoint that has the Marketplace trait to use.

        Send a ship to the waypoint to access trade good prices and recent transactions.
        Refer to the Market Overview page to gain better a understanding of the market in the game.
        """
        try:
            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/market",
            )

            response.raise_for_status()

            return (
                "Successfully fetched waypoint.",
                MarketResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_shipyard(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol.")],
        waypoint_symbol: Annotated[str, Field(description="The waypoint symbol.")],
    ) -> Tuple[str, ShipyardResponseSchema | None]:
        """Get the shipyard for a waypoint.

        Requires a waypoint that has the Shipyard trait to use.
        Send a ship to the waypoint to access data on ships that are currently available
        for purchase and recent transactions.
        """
        try:
            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/shipyard",
            )

            response.raise_for_status()

            print(response.json())

            return (
                "Successfully fetched shipyard.",
                ShipyardResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_jump_gate(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol.")],
        waypoint_symbol: Annotated[str, Field(description="The waypoint symbol.")],
    ) -> Tuple[str, JumpGateResponseSchema | None]:
        """Get jump gate details for a waypoint. Requires a waypoint of type JUMP_GATE to use.

        Waypoints connected to this jump gate can be ...
        """
        try:
            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/jump-gate",
            )

            response.raise_for_status()

            return (
                "Successfully fetched jump gate.",
                JumpGateResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_construction_site(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol.")],
        waypoint_symbol: Annotated[str, Field(description="The waypoint symbol.")],
    ) -> Tuple[str, ConstructionResponseSchema | None]:
        """Get construction details for a waypoint.

        Requires a waypoint with a property of isUnderConstruction to be true.
        """
        try:
            response = self.session.get(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/construction",
            )

            response.raise_for_status()

            return (
                "Successfully fetched construction site.",
                ConstructionResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def supply_construction_site(
        self,
        system_symbol: Annotated[str, Field(description="The system symbol.")],
        waypoint_symbol: Annotated[str, Field(description="The waypoint symbol.")],
        ship_symbol: Annotated[str, Field(description="Symbol of the ship to use.")],
        trade_symbol: Annotated[str, Field(description="The symbol of the good to supply.")],
        units: Annotated[int, Field(description="Amount of units to supply.")],
    ) -> Tuple[str, SupplyConstructionResponseSchema | None]:
        """Get construction details for a waypoint.

        Requires a waypoint with a property of isUnderConstruction to be true.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/construction",
                json={
                    "shipSymbol": ship_symbol,
                    "tradeSymbol": trade_symbol,
                    "units": units,
                }
            )

            response.raise_for_status()

            return (
                "Successfully fetched construction site.",
                SupplyConstructionResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None
