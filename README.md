# Coin-Predictor


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
PostgreSQL are orchestrated using Docker Compose. Configure the environment variables in a .env file located at the root of the project directory.

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
docker compose up
```

## Creating Database Tables
Before running the CLI commands to interact with the database, make sure you have created the database tables using Alembic migration models.

### Alembic Migration
To create the database tables, navigate to the api directory and run the following command:
```bash
alembic upgrade head
```
This command will apply all the migration scripts and create the tables defined in the Alembic models.


## Access postgres database
To access the database run this command:
```bash
docker exec -it postgres-db psql -U <POSTGRES_USER> -W <POSTGRES_DB>
```


## Cli
### Command 1: Single Query
This command performs a single query for a specific COIN and a specific date, which must be in `ISO8601 date` format. It then stores the extracted data in a CSV file in the `api/data/` folder. The file is named after the `coin` and the `date` like the following example: `bitcoin_2017-12-31.csv`
Run this command:
```bash
python3 cli.py one-query --coin bitcoin --date 2017-12-30
```
Options:
- `--coin`: Specifies the coin to query.
- `--date`: Specifies the date in YYYY-MM-DD format.


### Command 2: Massive Data Processing with Multithreading
This command performs queries for the coins bitcoin, ethereum, and cardano. It receives a start date and an end date in ISO8601 format yyyy-mm-dd as arguments. It processes data every day at `03:00 am` and stores the response data in a CSV file in the `data` directory with the following naming format: `coins_<start_date>_<end_date>.csv`.

It includes the option to load the data into a database with the `--load` flag.

Execute this command:
```bash
python3 cli.py run-multi-threading --start_date 2024-03-02 --end_date 2024-03-03 --max_threads 3 --load
```
Options:
- `--start_date`: Start date in yyyy-mm-dd format.
- `--end_date`: End date in yyyy-mm-dd format.
- `--max_threads`: Configurable number of threads.
- `--load`: Option to load the data into a database.


> [!NOTE]
> I have opted to configure the cron job using the Python library "schedule," which I found more intuitive than the Linux crontab. However, my conclusion is that using Airflow would have been more efficient.


## ​Analytical queries and script execution

All required queries for the task outlined in point 3 are stored in separate `.sql` files located in the `api/sql/queries/` directory. These files contain SQL queries needed for various database operations.

Additionally, there's a convenient script named `run_query.py` provided in the project root directory. This script automates the execution of the queries using SQLAlchemy. It streamlines the process, allowing for easy execution and testing of the queries against the configured database.