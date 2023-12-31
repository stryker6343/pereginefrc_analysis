import pytest
from fixtures import (INVALID_EVENT, VALID_EVENT, authenticated_client,
                      reports_data, unauthenticated_client)

from peregrinefrc_analysis.errors import MissingAccessTokenError


def test_event_reports_is_a_list(authenticated_client, reports_data):
    """Verify that the event_reports() method returns a list"""
    assert isinstance(reports_data, list)


def test_event_reports_dict_keys(authenticated_client, reports_data):
    """Verify that the report data contains the expected keys"""
    for report in reports_data:
        for key in ["teamKey", "matchKey", "realmId", "id", "eventKey", "data"]:
            assert key in report


def test_event_reports_invalid_event(authenticated_client):
    """Verify error handling of a invalid event"""
    with pytest.raises(ValueError) as _:
        authenticated_client.event_reports(INVALID_EVENT)


def test_event_reports_unauthenticated(unauthenticated_client):
    """Verify that calling a report function without authentications raises an error"""
    with pytest.raises(MissingAccessTokenError):
        unauthenticated_client.event_reports(VALID_EVENT)
