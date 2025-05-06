from explainshell-api import explain_command
from bs4 import BeautifulSoup
import pytest
import responses
    
def test_explain_command_parsing(sample_html):
    """Test parsing logic with mocked HTML."""
    cmd = "ls -lh --all"
    soup = BeautifulSoup(sample_html, 'html.parser')
    
    # Mock requests.get() response
    class MockResponse:
        text = sample_html
        def raise_for_status(self):
            pass
    
    # Test parsing
    result = explain_command(cmd)
    
    assert result['status'] == 'success'
    assert result['getargs'] == cmd
    assert len(result['matches']) == 4
    assert result['matches'][0]['match'] == 'ls'
    assert result['matches'][1]['helpclass'] == 'help-1'

def test_error_handling():
    """Test invalid command parsing."""
    with pytest.raises(ValueError):
        explain_command("invalid cmd")
        
@responses.activate
def test_integration_with_mocked_explainshell():
    """Mock explainshell.com response."""
    test_html = "<html><div id='command'>...</div></html>"
    responses.add(
        responses.GET,
        "http://explainshell:5000/explain?cmd=ls",
        body=test_html,
        status=200
    )
    
    result = explain_command("ls")
    assert 'matches' in result