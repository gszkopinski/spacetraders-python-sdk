"""Factions."""

from typing import Annotated, Tuple

import requests

from pydantic import Field

from ..models.models import (
    FactionResponseSchema,
    ListFactionsResponseSchema,
)


class Factions:
    """Factions."""

    def __init__(
        self,
        api_url: str,
        session: requests.Session,
    ) -> None:
        """Init."""
        self.api_url = api_url
        self.session = session

    def list_factions(
        self,
        page: Annotated[int, Field(description="What entry offset to request.", ge=1, default=1)] = 1,
        limit: Annotated[int, Field(description="How many entries to return per page.", ge=1, le=20, default=10)] = 10,
    ) -> Tuple[str, ListFactionsResponseSchema | None]:
        """Return a paginated list of all the factions in the game."""
        try:
            parameters = f"page={page}"
            parameters += f"&limit={limit}"

            response = self.session.get(
                url=f"{self.api_url}/factions?{parameters}",
            )

            response.raise_for_status()

            return (
                "Succesfully fetched factions.",
                ListFactionsResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "factions not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None

    def get_faction(
        self,
        faction_id: Annotated[str, Field(description="The faction ID.")]
    ) -> Tuple[str, FactionResponseSchema | None]:
        """Get the details of a faction by ID."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/factions/{faction_id}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched faction details.",
                FactionResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "faction not found.", None
                case _:
                    return f"Unknown error: {error.response.text}", None
