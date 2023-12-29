import sys

import requests
from os import getenv

BASE_URL = "https://api.peregrinefrc.com/"

# Get the server uptime
r = requests.get(BASE_URL)
print(f"Server Uptime: {r.json()['uptime']}")

# Log into the server using username / password stored in environment variables
username = getenv("PEREGRINE_USERNAME")
password = getenv("PEREGRINE_PASSWORD")
print(f"Username: {username}")

payload = {"username": username, "password": password}
r = requests.post(BASE_URL + "authenticate", json=payload)
if r.status_code != 200:
    print(r.status_code)
    print(r.text)
    sys.exit(1)
access_token = r.json()["accessToken"]
refresh_token = r.json()["refreshToken"]
print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")
security_header = {"Authorization": f"Bearer {access_token}"}

# Get the available years on the server
r = requests.get(BASE_URL + "years", headers=security_header)
print(f"Years: {r.json()}")

payload = {"year": 2023}
r = requests.get(BASE_URL + "events", headers=security_header, params=payload)
for event in r.json():
    print(f"{event['key']:10} {event['name']}")
