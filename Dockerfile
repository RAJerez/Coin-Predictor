FROM python:alpine3.10

# Configure Poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /api

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Run your app
COPY . /api/
COPY pyproject.toml poetry.lock
CMD [ "poetry", "run", "python", "-c" ]


