FROM python:3.5.2

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip poetry

RUN poetry install

CMD ["poetry", "run", "pytest", "--cov=telemetry"]