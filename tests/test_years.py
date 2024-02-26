from fixtures import authenticated_client


def test_years(authenticated_client):
    """Test that years() returns a list of integer years"""
    years = authenticated_client.years
    assert type(years) is list
    assert 2023 in years
    assert 2018 not in years  # Peregrine was first available in 2019
    assert len(years) >= 5
