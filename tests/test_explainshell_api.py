import pytest
import responses
from explainshell_api import explain_command
from tests import mock_explainshell_response, expected_output

@pytest.fixture(autouse=True)
def mock_response():
    """Automatically mock explainshell HTTP response for all tests."""
    with responses.RequestsMock() as rsps:
        mock_explainshell_response()
        yield rsps

def test_api_missing_and_invalid_param(client):
    """Should return 400 for missing or invalid 'cmd' parameters."""
    # Missing 'cmd'
    response = client.get("/api/explain")
    assert response.status_code == 400
    assert b'"error":"Missing cmd param"' in response.data

    # Invalid command
    response = client.get("/api/explain?cmd=invalidcommand")
    assert response.status_code == 400
    assert b'"error":"Invalid command"' in response.data

def test_api_valid_response(client):
    """Should return 200 and expected JSON for valid command."""
    response = client.get("/api/explain?cmd=ls+-lh+--all")
    assert response.status_code == 200
    data = response.get_json()
    assert data == expected_output
