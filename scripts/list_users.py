from os import getenv

from peregrinefrc_analysis import PeregrineClient

# EVENT_ID = "2024orwil"
# EXCLUDED_REPORTS = [9531, 9532]

client = PeregrineClient()
client.authenticate(
    username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
)
users = {}
for user in sorted(client.get_users(), key=lambda x: int(x["id"])):
    users[user["id"]] = (user["firstName"], user["firstName"])
    print(user["id"], user["firstName"], user["lastName"])
