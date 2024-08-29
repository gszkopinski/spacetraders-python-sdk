"""Client SDK for the SpaceTraders API."""

import sys

from os import environ
from typing import Optional

import requests

from dotenv import load_dotenv

from .models.models import StatusReponseSchema


from .agents import Agents
from .contracts import Contracts
from .factions import Factions
from .fleet import Fleet
from .systems import Systems


load_dotenv()


class SpaceTradersClient:
    """Client SDK for the SpaceTraders API."""

    def __init__(
        self,
        token: Optional[str] = None,
        api_url: Optional[str] = None,
    ) -> None:
        """Init the Client."""
        self.api_url = environ.get("API_URL", api_url)
        if not self.api_url:
            print("API URL not found")
            sys.exit(1)

        self.token = environ.get("TOKEN", token)
        if not self.token:
            print("TOKEN not found")
            sys.exit(1)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "Accept: application/json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )

        self.agents = Agents(
            api_url=self.api_url,
            session=self.session,
        )

        self.contracts = Contracts(
            api_url=self.api_url,
            session=self.session,
        )

        self.factions = Factions(
            api_url=self.api_url,
            session=self.session,
        )

        self.fleet = Fleet(
            api_url=self.api_url,
            session=self.session,
        )

        self.systems = Systems(
            api_url=self.api_url,
            session=self.session,
        )

    def get_status(
        self,
    ) -> StatusReponseSchema:
        """Return the status of the game server.

        This also includes a few global elements, such as announcements, server reset dates and leaderboards.
        """
        response = self.session.get(
            url=f"{self.api_url}/",
        )

        response.raise_for_status()

        return StatusReponseSchema.model_validate(response.json())
