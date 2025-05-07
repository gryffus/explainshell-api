# Explainshell API

Explainshell API is a lightweight JSON API wrapper for [explainshell](https://github.com/idank/explainshell). It takes shell commands as input and returns structured metadata for each component, including matched flags, commands, and their associated help text, with exact token positions. This makes it perfect for tools and frontend applications that need on-the-fly shell command explanations without scraping HTML. Ideal for interactive tutorials, terminal UIs, and intelligent CLI assistants.
![Tests](https://github.com/gryffus/explainshell-api/actions/workflows/python-tests.yml/badge.svg)
![Docker Build](https://github.com/gryffus/explainshell-api/actions/workflows/docker-build.yml/badge.svg)

---

## Features

- Parses and explains commands using explainshell
- Returns structured JSON responses with token positions
- Supports frontend and tool integration

---

## Installation

### 1. Clone `explainshell-api`

```bash
git clone https://github.com/gryffus/explainshell-api.git
cd explainshell-api
```

### 2. Initialize and update `explainshell`:

```bash
git submodule update --init --recursive
```

### 3. Download the database dump into the project root

```bash
curl -L -o ./dump.gz https://github.com/idank/explainshell/releases/download/db-dump/dump.gz
```

### 4. Build and run all services using Docker

```bash
docker-compose build
docker-compose up -d
```

This will start both the explainshell service and the API wrapper.

---

## Usage

You can now access the API at:

```
http://localhost:5000/api/explain?cmd=your+shell+command
```

Example:

```bash
curl "http://localhost:5000/api/explain?cmd=ls+-lh+--all"
```

### Sample Response

```json
{
   "getargs":"ls -lh --all",
   "helptext":[
      [
         "list directory contents",
         "help-0"
      ],
      [
         "<b>-l</b>     use a long listing format",
         "help-1"
      ],
      [
         "<b>-h</b>, <b>--human-readable</b>\n       with <b>-l</b>, print sizes in human readable format (e.g., 1K 234M 2G)",
         "help-2"
      ],
      [
         "<b>-a</b>, <b>--all</b>\n       do not ignore entries starting with .",
         "help-3"
      ]
   ],
   "matches":[
      {
         "commandclass":"command0",
         "end":2,
         "helpclass":"help-0",
         "match":"ls",
         "spaces":" ",
         "start":0,
         "suggestions":[
         ]
      },
      {
         "commandclass":"command0",
         "end":5,
         "helpclass":"help-1",
         "match":"-l",
         "spaces":" ",
         "start":3,
         "suggestions":[
         ]
      },
      {
         "commandclass":"command0",
         "end":6,
         "helpclass":"help-2",
         "match":"h",
         "spaces":" ",
         "start":5,
         "suggestions":[
         ]
      },
      {
         "commandclass":"command0",
         "end":12,
         "helpclass":"help-3",
         "match":"--all",
         "spaces":" ",
         "start":7,
         "suggestions":[
         ]
      }
   ],
   "status":"success"
}
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes
4. Submit a pull request

---

## License

This project wraps [explainshell](https://github.com/idank/explainshell), which is licensed under the MIT License. This wrapper is provided under the same license.
