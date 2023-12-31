from typing import NamedTuple


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


def get_count_stats(values: list[float]) -> CountStats:
    non_zero = [i for i in values if i != 0]
    if len(non_zero) == 0:
        non_zero = [
            0,
        ]
    return CountStats(
        quantity=len(values),
        average=sum(values) / len(values),
        maximum=max(values),
        minimum=min(values),
        minimum_other_than_zero=min(non_zero),
    )
