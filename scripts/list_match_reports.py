from os import getenv

from peregrinefrc_analysis import PeregrineClient


def main(event_ids, ignore_anonymous):
    client = PeregrineClient()
    client.authenticate(
        username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
    )

    users = client.scouter_info()
    user_db = {}
    for user in users:
        user_db[user["id"]] = f"{user["firstName"]} {user["lastName"]}"

    print("ID        EventKey   MatchKey  TeamKey  ReporterId  UserName")
    print("-" * 60)

    for event_report in client.event_reports(event_ids):
        reports = []
        for report in event_report:
            reporter_id = int(report["reporterId"])
            try:
                user_name = user_db[reporter_id]
            except KeyError:
                user_name = "Anonymous"
            reports.append(
                (
                    int(report["id"]),
                    report["eventKey"],
                    report["matchKey"],
                    report["teamKey"],
                    reporter_id,
                    user_name,
                )
            )

        reports.sort()
        for report in reports:
            id, event, match, team, user_id, user_name = report
            if ignore_anonymous == False or user_name != "Anonymous":
                print(f"{id:<8d}  {event:<10s} {match:<8s}  {team:<8s} {user_id:<10}  {user_name}")


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ignore_anonymous", action="store_true")
    parser.add_argument("event_ids", nargs="*")
    args = parser.parse_args()
    main(args.event_ids, args.ignore_anonymous)
