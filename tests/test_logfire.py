import pytest
from app.logfire import Logfire


@pytest.fixture
def logger():
    return Logfire(service_name="test_service")


def test_log_message(logger):
    assert logger is not None
    assert logger.service_name == "test_service"
    assert logger.token is not None
