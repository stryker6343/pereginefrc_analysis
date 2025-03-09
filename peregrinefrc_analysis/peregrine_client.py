from typing import Dict, Generator, List

import requests

from .errors import AuthenticationError, MissingAccessTokenError

DEFAULT_URL = "https://api.peregrinefrc.com/"


class PeregrineClient:
    def __init__(self, url: str = DEFAULT_URL):
        self._base_url = url
        self._access_token = ""
        self._refresh_token = ""
        self._years: List[int] = []

    def authenticate(self, username: str = "", password: str = ""):
        """Log into the Peregrine server"""
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
        """List of seasons available in Peregrine"""
        return self._years

    def event_reports(self, events: List[str]) -> Generator[Dict, None, None]:
        """Return all report data for a specific event"""
        if self._access_token:
            headers = {"Authorization": "Bearer " + self._access_token}
        else:
            raise MissingAccessTokenError(
                "The access token is not set, call the authenticate method first"
            )
        for event in events:
            payload = {"event": event}
            response = requests.get(
                self._base_url + "reports", params=payload, headers=headers
            )
            if response.status_code != 200:
                raise IOError(f"[Status {response.status_code}]: {response.text}")
            data = response.json()
            yield data

    def scouter_info(self):
        """Return scouter info"""
        if self._access_token:
            headers = {"Authorization": "Bearer " + self._access_token}
        else:
            raise MissingAccessTokenError(
                "The access token is not set, call the authenticate method first"
            )
        response = requests.get(self._base_url + "users", headers=headers)
        if response.status_code != 200:
            raise IOError(f"[Status {response.status_code}]: {response.text}")
        data = response.json()
        return data
