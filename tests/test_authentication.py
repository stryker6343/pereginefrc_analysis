from peregrinefrc_analysis.peregrine_client import PeregrineClient
from peregrinefrc_analysis.errors import AuthError
from os import getenv
import pytest


@pytest.fixture(scope="module")
def unauthenticated_client():
    """This client does not have an access token assigned"""
    return PeregrineClient()


@pytest.mark.parametrize(
    "username,password",
    [
        ("", ""),
        ("dummy", ""),
        ("", "invalidpassword"),
    ],
)
def test_authentication_blank_fields(unauthenticated_client, username, password):
    """This test checks for reporting of blank fields"""
    with pytest.raises(AuthError) as excinfo:
        unauthenticated_client.authenticate(username=username, password=password)
    error_message = str(excinfo.value)
    assert error_message.startswith("Authentication Error [Status 422]:")
    if len(username) == 0:
        assert (
            error_message.find(
                "Field validation for 'Username' failed on the 'gte' tag"
            )
            > 0
        )
    if len(password) == 0:
        assert (
            error_message.find(
                "Field validation for 'Password' failed on the 'gte' tag"
            )
            > 0
        )


def test_authentication_unauthorized(unauthenticated_client):
    """This test checks for handling of invalid username and password"""
    with pytest.raises(AuthError) as excinfo:
        unauthenticated_client.authenticate(
            username="dummy", password="invalidpassword"
        )
    error_message = str(excinfo.value)
    assert error_message.startswith("Authentication Error [Status 401]:")
    assert error_message.find("Unauthorized") > 0


def test_authentication_valid(unauthenticated_client):
    """This test verifies that a valid username and password works"""
    username = getenv("PEREGRINE_USERNAME")
    password = getenv("PEREGRINE_PASSWORD")
    unauthenticated_client.authenticate(username=username, password=password)
    assert unauthenticated_client._access_token is not None
    assert unauthenticated_client._refresh_token is not None
