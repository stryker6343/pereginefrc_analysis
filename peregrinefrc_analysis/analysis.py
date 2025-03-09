from collections import defaultdict
from collections.abc import Callable
import math
from typing import Any, Dict, NamedTuple, Sequence, List

from pandas import DataFrame

from . import BlueAllianceClient
from .peregrine_client import PeregrineClient


class TeamNumber:
    __slots__ = ("_team_id",)

    def __init__(self, team_id: str):
        if not team_id.startswith("frc"):
            raise ValueError(f"Value '{team_id}' does not start with 'frc'")
        if not team_id[3:].isnumeric():
            raise ValueError(f"Value '{team_id}' does not end with a number")
        self._team_id = team_id

    @property
    def number(self) -> int:
        return int(self._team_id[3:])

    @property
    def string(self) -> str:
        return self._team_id

    def __hash__(self):
        return hash(self._team_id)

    def __eq__(self, other):
        return self._team_id == other._team_id

    def __ne__(self, other):
        return not (self == other)


class Count(NamedTuple):
    team: TeamNumber
    value: float
    valid: bool


class CountStats(NamedTuple):
    quantity: float
    average: float
    maximum: float
    minimum: float
    minimum_other_than_zero: float
    standard_deviation: float


def is_valid_report(
    report: dict,
    excluded_realms: list[int] | None = None,
    excluded_reporters: list[int] | None = None,
    excluded_reports: list[int] | None = None,
) -> bool:
    """Tests if the report is valid"""
    result = True
    if excluded_realms and report["realmId"] in excluded_realms:
        result = False
    if excluded_reporters and report["reporterId"] in excluded_reporters:
        result = False
    if excluded_reports and report["id"] in excluded_reports:
        result = False
    return result


def get_count_stats(values: list[float]) -> CountStats:
    """Returns a CountStats object using the provided list of metric values"""
    non_zero = [i for i in values if i != 0]
    if len(non_zero) == 0:
        non_zero = [
            0,
        ]
    mean = sum(values) / len(values)
    variance = sum(pow(val - mean, 2) for val in values) / len(values)
    return CountStats(
        quantity=len(values),
        average=mean,
        maximum=max(values),
        minimum=min(values),
        minimum_other_than_zero=min(non_zero),
        standard_deviation=math.sqrt(variance),
    )


def count_metric(
    match_report: dict,
    match_fcn: Callable[[dict], bool],
    excluded_reports: list | None = None,
) -> Count:
    """Return a count of the specified metric using the report data and the
    provided counting function"""
    team_number = TeamNumber(match_report["teamKey"])
    total = 0
    valid = is_valid_report(match_report, excluded_reports=excluded_reports)
    for entry in match_report["data"]:
        if match_fcn(entry):
            total += entry["value"]
    return Count(team_number, total, valid)


def make_team_dataframe(
    client: PeregrineClient,
    events: List[str],
    count_names: Sequence[str],
    count_functions: Sequence[Callable[[dict], bool]],
    district_rankings: Dict[str, int] | None = None,
    excluded_reports: list | None = None,
) -> DataFrame:
    """Creates a Pandas DataFrame using Peregrine scouting data and the provided counting functions"""

    # District ranking points are optional. If missing, use an empty dict
    if district_rankings is None:
        district_rankings = {}

    # Determine the number of game pieces each team scored in each match
    counts: defaultdict[Any, List] = defaultdict(list)

    # For each provided counting function
    for i, fcn in enumerate(count_functions):

        # For each event, get all the scouting reports
        for reports in client.event_reports(events=events):

            # For each scouting report
            for report in reports:

                # Analyze the report using the given counting function
                team_number, value, valid_entry = count_metric(
                    report, fcn, excluded_reports=excluded_reports
                )

                # For each counting function, add another empty list
                if len(counts[team_number]) == i:
                    counts[team_number].append([])

                # If the report has not been excluded for some reason, include the count value in the results
                if valid_entry:
                    counts[team_number][i].append(value)

    # For each team, create a row with the count statistics of all counts
    data = []
    teams = []
    for team in counts:
        teams.append(team.number)
        row = []
        if len(district_rankings):
            row.append(district_rankings[team.string])
        for i, _ in enumerate(count_names):
            stats = get_count_stats(counts[team][i])
            row.extend([stats.minimum_other_than_zero, stats.average, stats.standard_deviation, stats.maximum])
        data.append(row)

    # Name the columns of the data frame
    # If provided, the first column district ranking points
    columns = ["DRP"] if len(district_rankings) else []

    # Then, add all count statistics to each row
    columns += [
        f"{i} {j}" for i in count_names for j in ["NZ Minimum", "Mean", "Std. Dev.", "Maximum"]
    ]

    return DataFrame(data, columns=columns, index=teams)
