from app.logfire import Logfire

logfire = Logfire(service_name="test_service")

def test_logfire_config():
    """
    Test the Logfire configuration.
    Assert that the token and service name are set correctly.
    """
    assert logfire.token is not None
    assert logfire.service_name == "test_service"