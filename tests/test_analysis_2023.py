from fixtures import authenticated_client
from peregrinefrc_analysis.analysis_2023 import make_team_dataframe
from pandas import DataFrame
from fixtures import VALID_EVENT


def test_make_team_dataframe(authenticated_client):
    """Verify it returns a dataframe"""
    team_dataframe = make_team_dataframe(authenticated_client, VALID_EVENT)
    assert isinstance(team_dataframe, DataFrame)
