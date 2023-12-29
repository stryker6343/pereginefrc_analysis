from peregrinefrc_analysis.peregrine_client import PeregrineClient
from os import getenv
import pytest


@pytest.fixture(scope="module")
def authenticated_client():
    """This client does not have an access token assigned"""
    client = PeregrineClient()
    username = getenv("PEREGRINE_USERNAME")
    password = getenv("PEREGRINE_PASSWORD")
    client.authenticate(username=username, password=password)
    return client


def test_years(authenticated_client):
    """Test that years() returns a list of integer years"""
    years = authenticated_client.years()
    assert type(years) is list
    assert 2023 in years
    assert 2018 not in years  # Peregrine was first available in 2019
    assert len(years) >= 5
