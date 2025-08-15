import pytest
from app.logfire import Logfire


@pytest.fixture
def logfire():
    return Logfire(service_name="test_service")


def test_logfire_initialization(logfire):
    """
    Test the logger initialization.
    Assert that the logger is created with the correct service name and token.
    """
    assert logfire.service_name == "test_service"
    assert logfire.token is not None
