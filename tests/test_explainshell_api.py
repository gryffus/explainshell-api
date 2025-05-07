import pytest
import responses
from explainshell_api import explain_command
from tests import mock_explainshell_response, expected_output

@pytest.fixture(autouse=True)
def mock_response():
    """Automatically mock the explainshell HTTP response."""
    with responses.RequestsMock() as rsps:
        # Register the mock response
        mock_explainshell_response()
        # Yield to run the test after the mock is set up
        yield rsps

@responses.activate
def test_explain_command_success():
    """Unit test: explain_command() returns expected parsed data."""
    cmd = "ls -lh --all"
    # Execute the command and check the result
    result = explain_command(cmd)
    # Assert that the result matches the expected output
    assert result == expected_output

def test_api_missing_param(client):
    """Integration test: return 400 for missing 'cmd'."""
    response = client.get("/explain")
    assert response.status_code == 400
    assert b'"error":"Missing cmd param"' in response.data

@responses.activate
def test_api_valid_response(client):
    """Integration test: GET /api/explain returns expected data."""
    response = client.get("/explain?cmd=ls+-lh+--all")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == expected_output
