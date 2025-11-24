import logging
from pathlib import Path
from importlib.resources import files
import tomllib


def get_data_file(name: str) -> Path:
    return files("convert_database_tool") / "SCRIPTS" / name


def get_config_file(name: str) -> Path:
    return files("convert_database_tool") / "configs" / name


def db_config_toml() -> dict:
    config_file = get_config_file(name="dbConfig.toml")
    with open(config_file, "rb") as file:
        return tomllib.load(file)["database_config"]


dbCons = db_config_toml()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

TABLES_SCRIPT = get_data_file(name="get_tables_to_convert.sql")
