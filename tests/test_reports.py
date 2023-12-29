from fixtures import authenticated_client
from fixtures import reports_data


def test_reports_is_a_list(authenticated_client, reports_data):
    """Verify that the reports method returns a list"""
    assert isinstance(reports_data, list)


def test_reports_dict_keys(authenticated_client, reports_data):
    """Verify that the report data contains the expected keys"""
    for report in reports_data:
        for key in ["teamKey", "matchKey", "realmId", "id", "eventKey", "data"]:
            assert key in report
