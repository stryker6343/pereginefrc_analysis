from .analysis import Count, TeamNumber, is_valid_report


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
    excluded_reports: list | None = None,
) -> Count:
    """Count the number of games pieces scored in the match report"""
    team_number = TeamNumber(match_report["teamKey"])
    total = 0
    valid = is_valid_report(
        match_report, excluded_realms, excluded_reporters, excluded_reports
    )
    for data in match_report["data"]:
        if "Cubes" in data["name"] or "Cones" in data["name"]:
            if is_valid_value(data["value"], max_value):
                total += data["value"]
    return Count(team_number, total, valid)


def count_total_game_pieces(entry_data: dict) -> bool:
    return "Cubes" in entry_data["name"] or "Cones" in entry_data["name"]


def count_total_cubes(entry_data: dict) -> bool:
    return "Cubes" in entry_data["name"]


def count_total_cones(entry_data: dict) -> bool:
    return "Cones" in entry_data["name"]


COUNT_FUNCTIONS = [
    count_total_game_pieces,
    count_total_cubes,
    count_total_cones,
]
COUNT_NAMES = [
    "Total Game Pieces",
    "Total Cubes",
    "Total Cones",
]
