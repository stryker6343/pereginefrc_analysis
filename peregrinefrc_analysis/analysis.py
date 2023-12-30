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


class Count(NamedTuple):
    team: TeamNumber
    value: float
    valid: bool
