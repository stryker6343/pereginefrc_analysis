from .errors import AuthError
import requests

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
            raise AuthError(response)
        data = response.json()
        self._access_token = data["accessToken"]
        self._refresh_token = data["refreshToken"]
        self._years = self._get_years()

    def _get_years(self) -> list[int]:
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.get(self._base_url + "years", headers=headers)
        # TODO: Add error handling code
        return response.json()

    @property
    def years(self) -> list[int]:
        return self._years

    def reports(self, event: str) -> list[dict]:
        """Return all report data for a specific event"""
        headers = {"Authorization": "Bearer " + self._access_token}
        payload = {"event": event}
        response = requests.get(
            self._base_url + "reports", params=payload, headers=headers
        )
        # TODO: Add error handling code
        return response.json()
