import pytest

from peregrinefrc_analysis.analysis import (Count, CountStats, TeamNumber,
                                            get_count_stats)


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


def test_get_count_stats_type():
    assert isinstance(get_count_stats([0, 1, 2, 3]), CountStats)


@pytest.mark.parametrize(
    "value,exp_qty,exp_min,exp_max,exp_ave,exp_min_otz",
    [
        ([0, 1, 2, 3], 4, 0, 3, 1.5, 1),
        ([0, 0, 0, 3], 4, 0, 3, 0.75, 3),
        ([0], 1, 0, 0, 0, 0),
    ],
)
def test_get_count_stats_values(value, exp_qty, exp_min, exp_max, exp_ave, exp_min_otz):
    result = get_count_stats(value)
    assert result.quantity == exp_qty
    assert result.minimum == exp_min
    assert result.maximum == exp_max
    assert result.average == exp_ave
    assert result.minimum_other_than_zero == exp_min_otz
