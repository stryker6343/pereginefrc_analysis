from typing import Dict

import requests


DEFAULT_URL = "https://www.thebluealliance.com/api/v3"


class BlueAllianceClient:

    def __init__(self, read_token: str, url: str = DEFAULT_URL):
        self._base_url = url
        self._read_token = read_token

    def district_rankings(self, district: str) -> Dict[str, int]:
        """Fetch the district ranking points for a given district (i.e. "2025pnw")"""

        # Download the ranking info from Blue Alliance
        payload = {"X-TBA-Auth-Key": self._read_token}
        response = requests.get(f"{self._base_url}/district/{district}/rankings", params=payload)
        data = response.json()

        # Return a mapping between a team key and its total district ranking points
        db = {}
        for team_data in data:
            db[team_data["team_key"]] = int(team_data["point_total"])
        return db
