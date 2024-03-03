FROM python:3.10-slim

# Configurar Poetry
ENV POETRY_VERSION=1.1.11
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false

# Instalar Poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

# Agregar las dependencias de la API
WORKDIR /api
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Copiar el resto del código de la API
COPY . .

# Ejecutar Alembic para migraciones de base de datos
RUN poetry run alembic upgrade head

# Ejecutar la API
CMD ["poetry", "run", "python", "app.py"]