from decouple import AutoConfig
from pathlib import Path

ROOT_DIR = Path().resolve()
DATA_DIR = ROOT_DIR / "data"

config = AutoConfig(search_path=ROOT_DIR)


DB_CONNSTR = config("DB_CONNSTR")
URL = config("URL")