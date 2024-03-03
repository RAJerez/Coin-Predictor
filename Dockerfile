FROM python:3.10-slim

ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}


ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /api

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY api/ .

RUN chmod +x /start.sh

RUN poetry run alembic upgrade head

CMD ["/start.sh"]