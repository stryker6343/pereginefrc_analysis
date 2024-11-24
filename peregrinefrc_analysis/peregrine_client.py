from typing import List, Optional

import requests

from .errors import AuthenticationError, MissingAccessTokenError

DEFAULT_URL = "https://api.peregrinefrc.com/"


class PeregrineClient:
    def __init__(self, url: str = DEFAULT_URL):
        self._base_url = url
        self._access_token = ""
        self._refresh_token = ""
        self._years: list[int] = []

    def authenticate(
        self, username: Optional[str] = "", password: Optional[str] = ""
    ) -> None:
        # username = username if username else ""
        # password = password if password else ""
        payload = {"username": username, "password": password}
        response = requests.post(self._base_url + "authenticate", json=payload)
        if response.status_code != 200:
            raise AuthenticationError(response)
        data = response.json()
        self._access_token = data["accessToken"]
        self._refresh_token = data["refreshToken"]
        self._years = self._get_years()

    def _get_years(self) -> List[int]:
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.get(self._base_url + "years", headers=headers)
        if response.status_code != 200:
            raise IOError(f"[Status {response.status_code}]: {response.text}")
        return response.json()

    @property
    def years(self) -> List[int]:
        return self._years

    def event_reports(self, event: str) -> List[dict]:
        """Return all report data for a specific event"""
        if self._access_token:
            headers = {"Authorization": "Bearer " + self._access_token}
        else:
            raise MissingAccessTokenError(
                "The access token is not set, call the authenticate method first"
            )
        payload = {"event": event}
        response = requests.get(
            self._base_url + "reports", params=payload, headers=headers
        )
        if response.status_code != 200:
            raise IOError(f"[Status {response.status_code}]: {response.text}")
        data = response.json()
        if len(data) == 0:
            raise ValueError(f"Event code '{event}' returned no event reports")
        return data
