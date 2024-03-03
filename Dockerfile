FROM python:alpine

WORKDIR /api/cli

COPY . /api
COPY pyproject.toml poetry.lock /api/

CMD [ "python3" , "cli.py" , ""]

# Aqui debe ir Poetry
RUN pip install -r requirements.txt


