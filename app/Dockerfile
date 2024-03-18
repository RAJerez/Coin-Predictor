FROM python:3.10-slim

ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY ../poetry.lock ./
COPY ../pyproject.toml ./
# COPY ../.env ./

RUN poetry install --no-interaction --no-root --no-dev

COPY . .

CMD ["poetry", "run", "./cli/cli.py"]

#RUN poetry run alembic upgrade head
#CMD ["python", "-c", "print('Hello, World!')"]