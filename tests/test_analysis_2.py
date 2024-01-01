import pytest
from fixtures import (
    INVALID_EVENT,
    VALID_EVENT,
    VALID_EVENT_SHAPE_2023,
    authenticated_client,
)
from pandas import DataFrame

from peregrinefrc_analysis.analysis import Count
from peregrinefrc_analysis.analysis import make_team_dataframe, count_metric
from peregrinefrc_analysis.analysis_2023 import (
    COUNT_NAMES,
    COUNT_FUNCTIONS,
    count_total_game_pieces,
)


def test_make_team_dataframe_type(authenticated_client):
    """Verify it returns a dataframe"""
    team_dataframe = make_team_dataframe(
        authenticated_client, VALID_EVENT, COUNT_NAMES, COUNT_FUNCTIONS
    )
    assert isinstance(team_dataframe, DataFrame)


def test_make_team_dataframe_shape(authenticated_client):
    """Verify it returns a dataframe"""
    team_dataframe = make_team_dataframe(
        authenticated_client, VALID_EVENT, COUNT_NAMES, COUNT_FUNCTIONS
    )
    assert team_dataframe.shape == VALID_EVENT_SHAPE_2023


def test_make_team_dataframe_with_invalid_event(authenticated_client):
    """Verify that creating a DataFrame with an invalid event raises an error"""
    with pytest.raises(ValueError) as excinfo:
        make_team_dataframe(
            authenticated_client, INVALID_EVENT, COUNT_NAMES, COUNT_FUNCTIONS
        )
        assert (
            str(excinfo.value)
            == f"ValueError: Event code '{INVALID_EVENT}' returned no event reports"
        )


TEST_REPORTS = [
    {
        "comment": "",
        "data": [
            {"name": "Top Cones (auto)", "value": 1},
            {"name": "Mid Cones (auto)", "value": 2},
            {"name": "Low Cones (auto)", "value": 3},
            {"name": "Top Cubes (auto)", "value": 4},
            {"name": "Mid Cubes (auto)", "value": 5},
            {"name": "Low Cubes (auto)", "value": 0},
            {"name": "Top Cones (teleop)", "value": 1},
            {"name": "Mid Cones (teleop)", "value": 2},
            {"name": "Low Cones (teleop)", "value": 3},
            {"name": "Top Cubes (teleop)", "value": 4},
            {"name": "Mid Cubes (teleop)", "value": 5},
            {"name": "Low Cubes (teleop)", "value": 0},
            {"name": "Played Defense", "value": 0},
            {"name": "Robot Died", "value": 0},
        ],
        "eventKey": "2023orwil",
        "id": 9545,
        "matchKey": "qm1",
        "realmId": 11,
        "reporterId": 421,
        "teamKey": "frc4450",
    },
    {
        "comment": "",
        "data": [
            {"name": "Top Cones (auto)", "value": 1},
            {"name": "Mid Cones (auto)", "value": 0},
            {"name": "Low Cones (auto)", "value": 3},
            {"name": "Top Cubes (auto)", "value": 4},
            {"name": "Mid Cubes (auto)", "value": 0},
            {"name": "Low Cubes (auto)", "value": 0},
            {"name": "Top Cones (teleop)", "value": 0},
            {"name": "Mid Cones (teleop)", "value": 0},
            {"name": "Low Cones (teleop)", "value": 0},
            {"name": "Top Cubes (teleop)", "value": 4},
            {"name": "Mid Cubes (teleop)", "value": 5},
            {"name": "Low Cubes (teleop)", "value": 0},
            {"name": "Played Defense", "value": 0},
            {"name": "Robot Died", "value": 0},
        ],
        "eventKey": "2023orwil",
        "id": 9546,
        "matchKey": "qm2",
        "realmId": 12,
        "reporterId": 423,
        "teamKey": "frc1234",
    },
    {
        "comment": "",
        "data": [
            {"name": "Top Cones (auto)", "value": 1},
            {"name": "Mid Cones (auto)", "value": 0},
            {"name": "Low Cones (auto)", "value": 3},
            {"name": "Top Cubes (auto)", "value": 4},
            {"name": "Mid Cubes (auto)", "value": 0},
            {"name": "Low Cubes (auto)", "value": 0},
            {"name": "Top Cones (teleop)", "value": 0},
            {"name": "Mid Cones (teleop)", "value": 0},
            {"name": "Low Cones (teleop)", "value": 0},
            {"name": "Top Cubes (teleop)", "value": 4},
            {"name": "Mid Cubes (teleop)", "value": 5},
            {"name": "Low Cubes (teleop)", "value": 0},
            {"name": "Played Defense", "value": 0},
            {"name": "Robot Died", "value": 0},
        ],
        "eventKey": "2023orwil",
        "id": 9547,
        "matchKey": "qm2",
        "realmId": 13,
        "reporterId": 424,
        "teamKey": "frc1234",
    },
]
EXCLUDED_REALMS = [13]
EXCLUDED_REPORTERS = [421]
EXCLUDED_REPORTS = [9546]

EXPECTED_VALUES = [30, 17, 17]
EXPECTED_VALUES_LESS_THAN_FIVE = [20, 12, 12]
EXPECTED_TEAMS = [4450, 1234, 1234]
EXPECTED_VALID_REALMS = [True, True, False]
EXPECTED_VALID_REPORTERS = [False, True, True]
EXPECTED_VALID_REPORTS = [True, False, True]


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_metric_type(index):
    assert isinstance(count_metric(TEST_REPORTS[index], count_total_game_pieces), Count)


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_metric_value(index):
    assert (
        count_metric(TEST_REPORTS[index], count_total_game_pieces).value
        == EXPECTED_VALUES[index]
    )


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_metric_valid(index):
    assert count_metric(TEST_REPORTS[index], count_total_game_pieces).valid is True


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_metric_team(index):
    assert (
        count_metric(TEST_REPORTS[index], count_total_game_pieces).team.number
        == EXPECTED_TEAMS[index]
    )


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_metric_match(index):
    assert (
        count_metric(
            TEST_REPORTS[index],
            count_total_game_pieces,
            excluded_reports=EXCLUDED_REPORTS,
        ).valid
        == EXPECTED_VALID_REPORTS[index]
    )
