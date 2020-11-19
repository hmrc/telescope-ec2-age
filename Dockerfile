FROM python:3.5.2

COPY . /app

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN rm -rf /root/.cache/pypoetry/artifacts
RUN poetry install -vvv
RUN poetry export -f requirements.txt > requirements.txt

CMD ["poetry", "run", "pytest", "--cov=telemetry"]