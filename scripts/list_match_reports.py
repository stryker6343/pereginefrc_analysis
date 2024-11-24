from os import getenv

from peregrinefrc_analysis import PeregrineClient

EVENT_ID = "2024orwil"
# EXCLUDED_REPORTS = [9531, 9532]

client = PeregrineClient()
client.authenticate(
    username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
)
reports = [
    (report["id"], report["matchKey"], report["reporterId"])
    for report in client.event_reports(EVENT_ID)
]
reports.sort()
for report in reports:
    print(*report)
