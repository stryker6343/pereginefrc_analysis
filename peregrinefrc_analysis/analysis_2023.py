from collections import defaultdict

from pandas import DataFrame

from .analysis import Count, CountStats, TeamNumber, get_count_stats
from .peregrine_client import PeregrineClient


def is_valid_report(
    report: dict,
    excluded_realms: list[int] | None,
    excluded_reporters: list[int] | None,
) -> bool:
    """Tests if the report is valid"""
    result = True
    if excluded_realms and report["realmId"] in excluded_realms:
        result = False
    if excluded_reporters and report["reporterId"] in excluded_reporters:
        result = False
    return result


def is_valid_value(value: int, max_value: int | None) -> bool:
    """Tests if the value is not greater than an optional max value"""
    result = True
    if max_value and value > max_value:
        result = False
    return result


def count_total_game_pieces_scored(
    match_report: dict,
    max_value: int | None = None,
    excluded_realms: list | None = None,
    excluded_reporters: list | None = None,
) -> Count:
    """Count the number of games pieces scored in the match report"""
    team_number = TeamNumber(match_report["teamKey"])
    total = 0
    valid = is_valid_report(match_report, excluded_realms, excluded_reporters)
    for data in match_report["data"]:
        if "Cubes" in data["name"] or "Cones" in data["name"]:
            if is_valid_value(data["value"], max_value):
                total += data["value"]
    return Count(team_number, total, valid)


def make_team_dataframe(client: PeregrineClient, event: str):
    """Creates a DataFrame with the stats from the given event"""
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
        teams.append(team.number)
        stats = get_count_stats(total_game_pieces_scored[team])
        data.append((stats.minimum_other_than_zero, stats.average, stats.maximum))

    return DataFrame(data, columns=["Minimum", "Average", "Maximum"], index=teams)
