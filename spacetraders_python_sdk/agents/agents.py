"""Agents."""

from typing import Annotated, Tuple

import requests

from pydantic import Field

from ..models.models import AgentResponseSchema, ListAgentsResponseSchema


class Agents:
    """Agents."""

    def __init__(
        self,
        api_url: str,
        session: requests.Session,
    ) -> None:
        """Init."""
        self.api_url = api_url
        self.session = session

    def get_agent(
        self,
    ) -> Tuple[str, AgentResponseSchema | None]:
        """Fetch your agent's details."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/my/agent",
            )

            response.raise_for_status()

            return (
                "Successfully fetched agent details.",
                AgentResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "Agent not found.", None
                case _:
                    return f"Unknown error: {error}", None

    def list_agents(
        self,
        page: Annotated[int, Field(description="What entry offset to request.", ge=1, default=1)] = 1,
        limit: Annotated[int, Field(description="How many entries to return per page.", ge=1, le=20, default=10)] = 10,
    ) -> Tuple[str, ListAgentsResponseSchema | None]:
        """Fetch agents details."""
        try:
            parameters = f"page={page}"
            parameters += f"&limit={limit}"

            response = self.session.get(
                url=f"{self.api_url}/agents?{parameters}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched agents details.",
                ListAgentsResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "Agents not found.", None
                case _:
                    return f"Unknown error: {error}", None

    def get_public_agent(
        self,
        agent_symbol: Annotated[str, Field(description="The agent symbol.", default="FEBA66")] = "FEBA66",
    ) -> Tuple[str, AgentResponseSchema | None]:
        """Fetch agent details."""
        try:
            response = self.session.get(
                url=f"{self.api_url}/agents/{agent_symbol}",
            )

            response.raise_for_status()

            return (
                "Successfully fetched agent details.",
                AgentResponseSchema.model_validate(response.json())
            )

        except requests.exceptions.HTTPError as error:
            match error.response.status_code:
                case 404:
                    return "Agent not found.", None
                case _:
                    return f"Unknown error: {error}", None
