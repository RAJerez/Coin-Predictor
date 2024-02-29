# Data-dev-exam-template

## Environment Setup

The project is compatible with any Python version `>= 3.8`. But I developed it with Python `3.10.12`


- Python >= 3.8
- Docker == 25.0.3 with Docker Compose.
- Poetry == 1.7.1 for efficient Python dependency management.


### Clone the repository:
```bash
git clone git@github.com:MuttData/exam-rodrigo-jerez.git
cd exam-rodrigo-jerez
```

### Poetry
If you do not have poetry installed, use this command:
```bash
pipx install poetry==1.7.1
```
`pipx` is used to install Python CLI applications globally while still isolating them in virtual environments.

Install project dependencies using Poetry:
```bash
poetry init
```
Activate the Poetry virtual environment:
```bash
poetry shell
```

### Setting environment variables for Docker
Airflow and PostgreSQL are orchestrated using Docker Compose. Configure the environment variables in a .env file located at the root of the project directory.

Create the `.env` file:
```bash
touch .env
```
Open the `.env` file in your IDE and set the environment variables with your credentials:
```
POSTGRES_USER=<your_user>
POSTGRES_PASSWORD=<your_password>
POSTGRES_DB=<your_database_name>
```

### Setting the settings.ini file
```
DB_CONNSTR=postgresql+psycopg2://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5432/<POSTGRES_DB>

URL=https://api.coingecko.com/api/v3/coins/
```


## Run Docker Compose
To initialize the containers, execute the following commands:
```bash
docker compose up airflow-init
docker compose up
```