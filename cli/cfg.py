from decouple import AutoConfig
from pathlib import Path


ROOT_DIR = str(Path().resolve())
DATA_DIR = ROOT_DIR + "/data"
LOG_DIR = ROOT_DIR + "/scripts/registry.log"

config = AutoConfig(search_path=ROOT_DIR)


DB_CONNSTR = config("DB_CONNSTR")
URL = config("URL")

TABLE_NAMES = ["coin_data", "coin_month_data"]