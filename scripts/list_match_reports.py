from os import getenv

from peregrinefrc_analysis import PeregrineClient

EVENT_IDS = ["2025orsal"]
# EXCLUDED_REPORTS = [9531, 9532]

client = PeregrineClient()
client.authenticate(
    username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
)

for event_report in client.event_reports(EVENT_IDS):
    reports = [
        (int(report["id"]), report["eventKey"], report["matchKey"], int(report["reporterId"]))
        for report in event_report
    ]
    reports.sort()
    for report in reports:
        print(*report)
