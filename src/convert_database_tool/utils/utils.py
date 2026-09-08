from .query import Conversion
from .constants import TABLES_SCRIPT, LOGGER
from neil import NeilPool
from enum import StrEnum, auto
import logging


class LoggingOptions(StrEnum):
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


def verbose_level(level: str) -> None:
    match LoggingOptions(level.strip().lower()):
        case LoggingOptions.INFO:
            LOGGER.setLevel(logging.INFO)
        case LoggingOptions.DEBUG:
            LOGGER.setLevel(logging.DEBUG)
        case LoggingOptions.WARNING:
            LOGGER.setLevel(logging.WARNING)
        case LoggingOptions.ERROR:
            LOGGER.setLevel(logging.ERROR)
        case LoggingOptions.CRITICAL:
            LOGGER.setLevel(logging.CRITICAL)
        case _:
            LOGGER.setLevel(logging.WARNING)


def run_conversions(dbPool: NeilPool):
    conv: Conversion = Conversion(dbPool=dbPool)
    database: str = str(dbPool.dbCons.get("database", ""))
    script: str = TABLES_SCRIPT.read_text().replace("<DATABASE_NAME>", database)
    dbPool.log.info(f"getting tables to convert for `{database}`...")
    conv.run_all(getting_sql_tables=script)
