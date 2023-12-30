import pytest

from peregrinefrc_analysis.analysis import TeamNumber
from peregrinefrc_analysis.analysis import Count


def test_analysis_team_number_type():
    assert isinstance(TeamNumber("frc1234"), TeamNumber)


@pytest.mark.parametrize("bad", ["ftc1234", "f1234"])
def test_analysis_team_number_bad_frc(bad):
    with pytest.raises(ValueError) as excinfo:
        TeamNumber(bad)
    assert str(excinfo.value) == f"Value '{bad}' does not start with 'frc'"


@pytest.mark.parametrize("bad", ["frc1234.3", "frcc12345"])
def test_analysis_team_number_bad_numeric(bad):
    with pytest.raises(ValueError) as excinfo:
        TeamNumber(bad)
    assert str(excinfo.value) == f"Value '{bad}' does not end with a number"


def test_analysis_count_type():
    assert isinstance(Count(team=TeamNumber("frc1234"), value=0, valid=True), Count)
