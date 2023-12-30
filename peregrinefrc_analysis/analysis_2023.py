from collections import defaultdict

from pandas import DataFrame

from .analysis import Count, TeamNumber
from .peregrine_client import PeregrineClient


def count_total_game_pieces_scored(
    match_report: dict,
    max_value: int | None = None,
    user_ids: list | None = None,
) -> Count:
    """Count the number of games pieces scored in the match report"""
    team_number = TeamNumber(match_report["teamKey"])
    total = 0
    valid = True
    for data in match_report["data"]:
        if "Cubes" in data["name"] or "Cones" in data["name"]:
            total += data["value"]
    return Count(team_number, total, valid)


def make_team_dataframe(client: PeregrineClient, event: str):
    reports = client.event_reports(event=event)

    # Determine the number of game pieces each team scored in each match
    total_game_pieces_scored = defaultdict(list)
    for report in reports:
        team_number, value, valid_entry = count_total_game_pieces_scored(report)
        if valid_entry:
            total_game_pieces_scored[team_number].append(value)

    # Find the min, max and value game pieces scored by each team
    data = []
    teams = []
    for team in total_game_pieces_scored:
        maximum = max(total_game_pieces_scored[team])
        average = sum(total_game_pieces_scored[team]) / len(
            total_game_pieces_scored[team]
        )
        filtered_count = [i for i in total_game_pieces_scored[team] if i != 0]
        minimum = min(filtered_count, default=0)
        teams.append(team.number)
        data.append((minimum, average, maximum))

    return DataFrame(data, columns=["Minimum", "Average", "Maximum"], index=teams)
