import pytest
from fixtures import VALID_EVENT, authenticated_client
from pandas import DataFrame

from peregrinefrc_analysis.analysis import Count
from peregrinefrc_analysis.analysis_2023 import (
    count_total_game_pieces_scored, make_team_dataframe)


def test_make_team_dataframe(authenticated_client):
    """Verify it returns a dataframe"""
    team_dataframe = make_team_dataframe(authenticated_client, VALID_EVENT)
    assert isinstance(team_dataframe, DataFrame)


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
        "id": 9546,
        "matchKey": "qm2",
        "realmId": 13,
        "reporterId": 424,
        "teamKey": "frc1234",
    },
]
EXCLUDED_REALMS = [13]
EXCLUDED_REPORTERS = [421]
EXPECTED_VALUES = [30, 17, 17]
EXPECTED_VALUES_LESS_THAN_FIVE = [20, 12, 12]
EXPECTED_TEAMS = [4450, 1234, 1234]
EXPECTED_VALID_REALMS = [True, True, False]
EXPECTED_VALID_REPORTERS = [False, True, True]


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_type(index):
    assert isinstance(count_total_game_pieces_scored(TEST_REPORTS[index]), Count)


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_value(index):
    assert (
        count_total_game_pieces_scored(TEST_REPORTS[index]).value
        == EXPECTED_VALUES[index]
    )


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_valid(index):
    assert count_total_game_pieces_scored(TEST_REPORTS[index]).valid is True


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_team(index):
    assert (
        count_total_game_pieces_scored(TEST_REPORTS[index]).team.number
        == EXPECTED_TEAMS[index]
    )


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_value_4_max(index):
    assert (
        count_total_game_pieces_scored(TEST_REPORTS[index], max_value=4).value
        == EXPECTED_VALUES_LESS_THAN_FIVE[index]
    )


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_valid_realm(index):
    assert (
        count_total_game_pieces_scored(
            TEST_REPORTS[index], excluded_realms=EXCLUDED_REALMS
        ).valid
        == EXPECTED_VALID_REALMS[index]
    )


@pytest.mark.parametrize("index", list(range(len(TEST_REPORTS))))
def test_count_total_game_pieces_scored_valid_reporter(index):
    assert (
        count_total_game_pieces_scored(
            TEST_REPORTS[index], excluded_reporters=EXCLUDED_REPORTERS
        ).valid
        == EXPECTED_VALID_REPORTERS[index]
    )
