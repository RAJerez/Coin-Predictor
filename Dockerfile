FROM python:3.10-slim

ENV POETRY_VERSION=1.1.11
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

WORKDIR /api
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

RUN poetry run alembic upgrade head

CMD ["poetry", "run", "python", "app.py"]