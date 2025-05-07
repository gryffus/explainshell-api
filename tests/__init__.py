import responses

def mock_explainshell_response():
    mock_html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>explainshell.com - ls -lh --all</title>
        </head>
        <body data-theme=dark>
            <div class="container">
                <div id="command">
                    <span class="dropdown">
                        <span style="word-spacing: 0px;">
                            <span class="command0 simplecommandstart" helpref="help-0"><a href="/explain/1/ls">ls(1)</a></span>
                        </span>
                    </span>
                    <span class="command0" helpref="help-1">-l</span>
                    <span class="command0" helpref="help-2">h</span>
                    <span class="command0" helpref="help-3">--all</span>
                </div>
                <table id="help">
                    <tbody>
                        <tr><td><pre class="help-box" id="help-0">list directory contents</pre></td></tr>
                        <tr><td><pre class="help-box" id="help-1"><b>-l</b>     use a long listing format</pre></td></tr>
                        <tr><td><pre class="help-box" id="help-2"><b>-h</b>, <b>--human-readable</b>\n       with <b>-l</b>, print sizes in human readable format (e.g., 1K 234M 2G)</pre></td></tr>
                        <tr><td><pre class="help-box" id="help-3"><b>-a</b>, <b>--all</b>\n       do not ignore entries starting with .</pre></td></tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """

    responses.add(
        responses.GET,
        "http://explainshell:5000/api/explain?cmd=ls+-lh+--all",
        body=mock_html,
        status=200
    )

expected_output = {
    "getargs": "ls -lh --all",
    "helptext": [
        ["list directory contents", "help-0"],
        ["<b>-l</b>     use a long listing format", "help-1"],
        ["<b>-h</b>, <b>--human-readable</b>\n       with <b>-l</b>, print sizes in human readable format (e.g., 1K 234M 2G)", "help-2"],
        ["<b>-a</b>, <b>--all</b>\n       do not ignore entries starting with .", "help-3"]
    ],
    "matches": [
        {"commandclass": "command0", "end": 2, "helpclass": "help-0", "match": "ls", "spaces": " ", "start": 0, "suggestions": []},
        {"commandclass": "command0", "end": 5, "helpclass": "help-1", "match": "-l", "spaces": " ", "start": 3, "suggestions": []},
        {"commandclass": "command0", "end": 6, "helpclass": "help-2", "match": "h", "spaces": " ", "start": 5, "suggestions": []},
        {"commandclass": "command0", "end": 12, "helpclass": "help-3", "match": "--all", "spaces": " ", "start": 7, "suggestions": []}
    ],
    "status": "success"
}
