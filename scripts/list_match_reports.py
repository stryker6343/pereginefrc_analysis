from os import getenv

from peregrinefrc_analysis import PeregrineClient

EVENT_IDS = ["2025orsal"]

client = PeregrineClient()
client.authenticate(
    username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
)

users = client.scouter_info()
user_db = {}
for user in users:
    user_db[user["id"]] = f"{user["firstName"]} {user["lastName"]}"

for event_report in client.event_reports(EVENT_IDS):
    reports = []
    for report in event_report:
        reporter_id = int(report["reporterId"])
        try:
            user_name = user_db[reporter_id]
        except KeyError:
            user_name = "Anonymous"
        reports.append((int(report["id"]), report["eventKey"], report["matchKey"], reporter_id, user_name))

    reports.sort()
    for report in reports:
        print(*report)
