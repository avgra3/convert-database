import mariadb
from multiprocessing import cpu_count, Pool, freeze_support
from .constants import LOGGER
from logging import Logger


class Conversion:
    def __init__(self, dbCons: dict[str, any], log: Logger = LOGGER):
        self.pool_size = min(cpu_count() // 2, 16)
        self.log = log
        self.dbCons = dbCons
        self.pool_number = 0

    def getTablesToConvert(self, script: str) -> list[tuple[str]]:
        results = []
        try:
            with mariadb.connect(**self.dbCons) as conn:
                cur = conn.cursor()
                cur.execute(script)
                results = cur.fetchall()
        except Exception as e:
            self.log.critical(
                "An exception occured, please review the error given"
            )
            self.log.critical(e)
        return results

    def run_queries(self, queries: list[tuple[str]]) -> None:
        for sql_scripts in queries:
            for split in sql_scripts.split(";"):
                if split.strip() == "":
                    continue
                try:
                    with mariadb.connect(self.dbCons) as conn:
                        cur = conn.cursor()
                        cur.execute(statement=split)
                        cur.close()
                except mariadb.ProgrammingError as e:
                    self.log.warning("An exception occured.")
                    self.log.warning("Exception occured while running:")
                    self.log.warning(split)
                    self.log.warning("Please review the error given.")
                    self.log.warning(e)
                except mariadb.Error as e:
                    error_message = "An occured while running the previous sql"
                    error_message += " Review the error message for details."
                    self.log.error(error_message)
                    self.log.error(e)

    def run_alters_mp(self, alters: list[tuple[str]]):
        if len(alters) < self.pool_size:
            self.pool_size = len(alters)
        freeze_support()
        with Pool(processes=self.pool_size) as pool:
            pool.map(self.run_queries, alters)
