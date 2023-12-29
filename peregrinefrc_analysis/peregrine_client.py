from .errors import AuthError
import requests

DEFAULT_URL = "https://api.peregrinefrc.com/"


class PeregrineClient:
    def __init__(self, url: str = DEFAULT_URL):
        self._base_url = url
        self._access_token = None
        self._refresh_token = None

    def authenticate(self, username: str, password: str):
        payload = {"username": username, "password": password}
        response = requests.post(self._base_url + "authenticate", json=payload)
        if response.status_code != 200:
            raise AuthError(response)
        data = response.json()
        self._access_token = data["accessToken"]
        self._refresh_token = data["refreshToken"]

    def years(self):
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.get(self._base_url + "years", headers=headers)
        # TODO: Add error handling code
        return response.json()
