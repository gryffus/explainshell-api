import pytest
import responses
from explainshell_api import explain_command
from tests import mock_explainshell_response, expected_output

@pytest.fixture(autouse=True)
def mock_response():
    """Automatically mock the explainshell HTTP response."""
    with responses.RequestsMock() as rsps:
        mock_explainshell_response()
        yield rsps

def test_explain_command_success():
    """Unit test: explain_command() returns expected parsed data."""
    cmd = "ls -lh --all"
    result = explain_command(cmd)
    assert result == expected_output

def test_api_missing_and_invalid_param(client):
    """Integration test: return 400 for missing or invalid 'cmd'."""
    response = client.get("/explain")
    assert response.status_code == 400
    assert b'"error":"Missing cmd param"' in response.data

    response = client.get("/explain?cmd=invalidcommand")
    assert response.status_code == 400 or response.status_code == 500  # depends on implementation
    assert b'"error":"' in response.data

def test_api_valid_response(client):
    """Integration test: GET /api/explain returns expected data."""
    response = client.get("/explain?cmd=ls+-lh+--all")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == expected_output
