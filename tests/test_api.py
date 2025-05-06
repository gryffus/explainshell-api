def test_api_endpoint(client):
    """Test /api/explain with valid command."""
    response = client.get("/api/explain?cmd=ls+-lh")
    assert response.status_code == 200
    assert b'"status":"success"' in response.data

def test_api_missing_param(client):
    """Test missing 'cmd' parameter."""
    response = client.get("/api/explain")
    assert response.status_code == 400
    assert b'"error":"Missing cmd param"' in response.data