"""Fleet."""

from typing import Annotated, Tuple

import requests

from pydantic import Field

from ..models.models import (
    CreateSurveyResponseSchema,
    ExtractResponseSchema,
    ListShipsResponseSchema,
    NavigateShipResponseSchema,
    RefuelShipResponseSchema,
    SellCargoResponseSchema,
    ShipCargoResponseSchema,
    ShipOrbitResponseSchema,
    ShipResponseSchema,
    SurveySchema,
    TradeGoodSchema,
)


class Fleet:
    """Fleet."""

    def __init__(
        self,
        api_url: str,
        session: requests.Session,
    ) -> None:
        """Init."""
        self.api_url = api_url
        self.session = session

    def list_ships(
        self,
        page: Annotated[int, Field(description="What entry offset to request.", ge=1, default=1)] = 1,
        limit: Annotated[int, Field(description="How many entries to return per page.", ge=1, le=20, default=10)] = 10,
    ) -> Tuple[str, ListShipsResponseSchema | None]:
        """Return a paginated list of all the ships in the game."""
        try:
            parameters = f"page={page}"
            parameters += f"&limit={limit}"

            response = self.session.get(
                url=f"{self.api_url}/my/ships?{parameters}",
            )

            response.raise_for_status()

            return (
                "Succesfully fetched ships.",
                ListShipsResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_ship(
        self,
        ship_symbol: Annotated[str, Field(description="The ship ID.")],
    ) -> Tuple[str, ShipResponseSchema | None]:
        """Get the details of a ship by ID."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/my/ships/{ship_symbol}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched ship details.",
                ShipResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_ship_cargo(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
    ) -> Tuple[str, ShipCargoResponseSchema | None]:
        """Retrieve the cargo of a ship under your agent's ownership."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/my/ships/{ship_symbol}/cargo",
            )

            response.raise_for_status()

            return (
                "Successfully fetched ship's cargo.",
                ShipCargoResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def orbit_ship(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
    ) -> Tuple[str, ShipOrbitResponseSchema | None]:
        """Attempt to move your ship into orbit at its current location.

        The request will only succeed if your ship is capable of moving into orbit at the time of the request.
        Orbiting ships are able to do actions that require the ship to be above surface such as navigating or
        extracting, but cannot access elements in their current waypoint, such as the market or a shipyard.

        The endpoint is idempotent - successive calls will succeed even if the ship is already in orbit.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/orbit",
            )

            response.raise_for_status()

            return (
                "The ship has successfully moved into orbit at its current location.",
                ShipOrbitResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def navigate_ship(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
        waypoint_symbol: Annotated[str, Field(description="The target destination.")]
    ) -> Tuple[str, NavigateShipResponseSchema | None]:
        """Navigate to a target destination.

        The ship must be in orbit to use this function.
        The destination waypoint must be within the same system as the ship's current location.
        Navigating will consume the necessary fuel from the ship's manifest based on the distance
        to the target waypoint.

        The returned response will detail the route information including the expected time of arrival
        Most ship actions are unavailable until the ship has arrived at it's destination.

        To travel between systems, see the ship's Warp or Jump actions.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/navigate",
                json={
                    "waypointSymbol": waypoint_symbol
                }
            )

            response.raise_for_status()

            return (
                (
                    "The successful transit information including the route details and changes to ship fuel."
                    "The route includes the expected time of arrival."
                ),
                NavigateShipResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def dock_ship(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
    ) -> Tuple[str, ShipOrbitResponseSchema | None]:
        """Attempt to dock your ship at its current location.

        Docking will only succeed if your ship is capable of docking at the time of the request.

        Docked ships can access elements in their current location,
        such as the market or a shipyard, but cannot do actions that requir
        the ship to be above surface such as navigating or extracting.

        The endpoint is idempotent - successive calls will succeed even if the ship is already docked.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/dock",
            )

            response.raise_for_status()

            return (
                "The ship has successfully docked at its current location.",
                ShipOrbitResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def refuel_ship(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
        units: Annotated[
            int,
            Field(
                description=(
                    "The amount of fuel to fill in the ship's tanks."
                    "When not specified, the ship will be refueled to its maximum fuel capacity."
                    "If the amount specified is greater than the ship's remaining capacity,"
                    "the ship will only be refueled to its maximum fuel capacity."
                    "The amount specified is not in market units but in ship fuel units."
                ),
                ge=1,
            )
        ] = 100,
        from_cargo: Annotated[
            bool,
            Field(description="Wether to use the FUEL thats in your cargo or not. Default: false")
        ] = False,
    ) -> Tuple[str, RefuelShipResponseSchema | None]:
        """Refuel your ship by buying fuel from the local market.

        Requires the ship to be docked in a waypoint that has the Marketplace trait,
        and the market must be selling fuel in order to refuel.

        Each fuel bought from the market replenishes 100 units in your ship's fuel.

        Ships will always be refuel to their frame's maximum fuel capacity when using this action.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/refuel",
                json={
                    "units": units,
                    "fromCargo": from_cargo,
                }
            )

            response.raise_for_status()

            return (
                "The ship has successfully docked at its current location.",
                RefuelShipResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def extract_resources(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
    ) -> Tuple[str, ExtractResponseSchema | None]:
        """Extract resources from a waypoint that can be extracted, such as asteroid fields, into your ship.

        Send an optional survey as the payload to target specific yields.

        The ship must be in orbit to be able to extract and must have mining equipments installed
        that can extract goods, such as the Gas Siphon mount for gas-based goods
        or Mining Laser mount for ore-based goods.

        The survey property is now deprecated. See the extract/survey endpoint for more details.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/extract",
            )

            response.raise_for_status()

            return (
                "Extracted successfully.",
                ExtractResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def create_survey(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
    ) -> Tuple[str, CreateSurveyResponseSchema | None]:
        """Create surveys on a waypoint that can be extracted such as asteroid fields.
        A survey focuses on specific types of deposits from the extracted location.
        When ships extract using this survey,
        they are guaranteed to procure a high amount of one of the goods in the survey.

        In order to use a survey, send the entire survey details in the body of the extract request.

        Each survey may have multiple deposits, and if a symbol shows up more than once,
        that indicates a higher chance of extracting that resource.

        Your ship will enter a cooldown after surveying in which it is unable to perform certain actions.
        Surveys will eventually expire after a period of time or will be exhausted after being extracted several times
        based on the survey's size.
        Multiple ships can use the same survey for extraction.

        A ship must have the Surveyor mount installed in order to use this function.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/survey",
            )

            response.raise_for_status()

            return (
                "Surveys has been created.",
                CreateSurveyResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def extract_resources_with_survey(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
        survey: Annotated[SurveySchema, Field(description=(
            "A resource survey of a waypoint, detailing a specific extraction location and the types of resources"
            "that can be found there."
        ))],
    ) -> Tuple[str, ExtractResponseSchema | None]:
        """Extract resources from a waypoint that can be extracted, such as asteroid fields, into your ship.

        Send an optional survey as the payload to target specific yields.

        The ship must be in orbit to be able to extract and must have mining equipments installed
        that can extract goods, such as the Gas Siphon mount for gas-based goods
        or Mining Laser mount for ore-based goods.

        The survey property is now deprecated. See the extract/survey endpoint for more details.
        """
        try:
            deposit_list = []
            for deposit in survey.deposits:
                deposit_list.append({"symbol": deposit.symbol})
            survey_json = {
                "signature": survey.signature,
                "symbol": survey.symbol,
                "deposits": deposit_list,
                "expiration": survey.expiration,
                "size": survey.size.value,
            }
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/extract/survey",
                json=survey_json,
            )

            response.raise_for_status()

            return (
                "Extracted successfully.",
                ExtractResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None

    def sell_cargo(
        self,
        ship_symbol: Annotated[str, Field(description="The symbol of the ship.")],
        symbol: Annotated[TradeGoodSchema, Field(description="The good's symbol.")],
        units: Annotated[int, Field(description="Amounts of units to sell of the selected good.")],
    ) -> Tuple[str, SellCargoResponseSchema | None]:
        """Sell cargo in your ship to a market that trades this cargo.

        The ship must be docked in a waypoint that has the Marketplace trait in order to use this function.
        """
        try:
            response = self.session.post(
                url=f"{self.api_url}/my/ships/{ship_symbol}/sell",
                json={
                    "symbol": symbol,
                    "units": units,
                }
            )

            response.raise_for_status()

            return (
                "Cargo was successfully sold.",
                SellCargoResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case _:
                    return f"Unknown error: {error.response.text}", None
