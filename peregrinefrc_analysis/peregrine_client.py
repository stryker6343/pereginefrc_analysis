import requests

from .errors import AuthenticationError, MissingAccessTokenError

DEFAULT_URL = "https://api.peregrinefrc.com/"


class PeregrineClient:
    def __init__(self, url: str = DEFAULT_URL):
        self._base_url = url
        self._access_token = None
        self._refresh_token = None
        self._years = None

    def authenticate(self, username: str, password: str) -> None:
        payload = {"username": username, "password": password}
        response = requests.post(self._base_url + "authenticate", json=payload)
        if response.status_code != 200:
            raise AuthenticationError(response)
        data = response.json()
        self._access_token = data["accessToken"]
        self._refresh_token = data["refreshToken"]
        self._years = self._get_years()

    def _get_years(self) -> list[int]:
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.get(self._base_url + "years", headers=headers)
        if response.status_code != 200:
            raise IOError(f"[Status {response.status_code}]: {response.text}")
        return response.json()

    @property
    def years(self) -> list[int]:
        return self._years

    def event_reports(self, event: str) -> list[dict]:
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
