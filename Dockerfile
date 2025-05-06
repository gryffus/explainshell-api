FROM python:2.7

WORKDIR /app

COPY explainshell_api.py .

RUN pip install flask requests beautifulsoup4

ENV FLASK_APP=/app/explainshell_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

CMD ["flask", "run"]