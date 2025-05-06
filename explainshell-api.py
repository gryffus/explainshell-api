#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
File: explainshell-api.py
Author: Lukáš Krejza (gryffus@hkfree.org)
GitHub: https://github.com/gryffus/explainshell-api
Description: JSON API for explainshell — structured shell command explanations for dev tools and UIs.
License: MIT (or other license)
Created: 2025-05-06
Last Modified: 2025-05-06
Version: 0.1.0
"""

from flask import Flask, request, jsonify
import os
import requests
import urllib
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

EXPLAINSHELL_HOST = os.getenv("EXPLAINSHELL_HOST", "explainshell")
EXPLAINSHELL_PORT = os.getenv("EXPLAINSHELL_PORT", "5000")
base_path = os.getenv("API_PATH", "").rstrip('/')
route_path = base_path + "/explain" if base_path else "/explain"

def explain_command(cmd):
    encoded_cmd = urllib.quote_plus(cmd)
    url = "http://{}:{}/explain?cmd={}".format(EXPLAINSHELL_HOST, EXPLAINSHELL_PORT, encoded_cmd)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    command_spans = soup.select('#command span.command0')
    help_texts = soup.select('#help pre.help-box')
    matches = []
    helptext = []
    i = 0
    tag_index = 0
    result = []
    cursor = 0
    for span in command_spans:
        a_tag = span.find('a')
        if a_tag:
            command = a_tag.text.strip().split('(')[0]
        else:
            command = span.get_text()
        helpref = span.get('helpref')
        help_html = help_texts[tag_index].decode_contents() if tag_index < len(help_texts) else ""
        while cursor < len(cmd) and cmd[cursor] == ' ':
            cursor += 1
        start = cursor
        end = start + len(command)
        if cmd[start:end] != command:
            raise ValueError("Parsing error: expected '{}' at position {}, found '{}'".format(
                command, start, cmd[start:end]
            ))
        matches.append({
            "commandclass": "command0",
            "helpclass": helpref,
            "match": command,
            "start": start,
            "end": end,
            "spaces": " " if start > 0 and cmd[start - 1] == " " else "",
            "suggestions": []
        })
        result.append({
            "helpHTML": help_html,
            "start": start,
            "end": end
        })
        cursor = end
        tag_index += 1
    output = {
        'getargs': cmd,
        'helptext': [[help_texts[i].decode_contents(), 'help-' + str(i)] for i in range(len(help_texts))],
        'matches': matches,
        'status': 'success'
    }
    return output

@app.route(route_path, methods=["GET"])
def explain():
    cmd = request.args.get("cmd", "")
    if not cmd:
        return jsonify({"error": "Missing cmd param"}), 400
    try:
        output = explain_command(cmd)
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500