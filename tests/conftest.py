import pytest
from explainshell_api import app as flask_app
from bs4 import BeautifulSoup

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_html():
    return """
    <html>
        <div id="command">
            <span class="command0" helpref="help-0"><a href="/explain/1/ls">ls(1)</a></span>
            <span class="command0" helpref="help-1">-l</span>
            <span class="command0" helpref="help-2">h</span>
            <span class="command0" helpref="help-3">--all</span>
        </div>
        <table id="help">
            <tr><td><pre class="help-box" id="help-0">list directory contents</pre></td></tr>
            <tr><td><pre class="help-box" id="help-1"><b>-l</b> use long format</pre></td></tr>
        </table>
    </html>
    """