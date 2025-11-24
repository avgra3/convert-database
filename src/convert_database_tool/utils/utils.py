from .query import Conversion
from .constants import dbCons, TABLES_SCRIPT, LOGGER


def getTablesToConvert(database: str) -> list[tuple[str]]:
    dbCons["database"] = database
    conv = Conversion(dbCons=dbCons)
    script = TABLES_SCRIPT.read_text().replace("<DATABASE_NAME>", database)
    LOGGER.info(f"getting tables to convert for `{database}`...")
    results = conv.getTablesToConvert(script=script)
    return results


def alterTables(database: str, alters: list[tuple[str]]) -> None:
    dbCons["database"] = database
    conv = Conversion(dbCons=dbCons)
    LOGGER.info(f"converting tables for `{database}`...")
    conv.run_alters_mp(alters=alters)
